"""
Project service for managing structural analysis projects.

Provides high-level operations for:
- Creating new projects
- Opening existing projects
- Saving projects
- Managing recent projects list
- Auto-save functionality
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from paz.core.constants import AUTOSAVE_INTERVAL_SECONDS, MAX_RECENT_PROJECTS
from paz.core.exceptions import FileError
from paz.core.logging_config import get_logger
from paz.core.units import SI_UNITS, UnitSystem
from paz.domain.model.project import Project, ProjectFile
from paz.infrastructure.repositories.file_repository import FileRepository


logger = get_logger("project_service")


class RecentProject:
    """Represents a recently opened project."""

    def __init__(self, path: str, name: str, opened_at: datetime) -> None:
        self.path = path
        self.name = name
        self.opened_at = opened_at

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "path": self.path,
            "name": self.name,
            "opened_at": self.opened_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RecentProject":
        """Create from dictionary."""
        return cls(
            path=data["path"],
            name=data["name"],
            opened_at=datetime.fromisoformat(data["opened_at"]),
        )


class ProjectService:
    """
    Service for managing PAZ projects.

    Handles project lifecycle including creation, saving, loading,
    and recent projects management.
    """

    def __init__(
        self,
        file_repository: FileRepository | None = None,
        settings_path: Path | None = None,
    ) -> None:
        """
        Initialize the project service.

        Args:
            file_repository: Repository for file operations
            settings_path: Path to store settings (recent projects, etc.)
        """
        self.file_repository = file_repository or FileRepository()
        self.settings_path = settings_path or Path.home() / ".paz" / "settings.json"
        self._current_project: ProjectFile | None = None
        self._current_path: Path | None = None
        self._recent_projects: list[RecentProject] = []
        self._load_settings()

    @property
    def current_project(self) -> ProjectFile | None:
        """Get the currently open project."""
        return self._current_project

    @property
    def current_path(self) -> Path | None:
        """Get the path of the currently open project."""
        return self._current_path

    @property
    def is_dirty(self) -> bool:
        """Check if the current project has unsaved changes."""
        # TODO: Implement change tracking
        return self._current_project is not None

    def create_project(
        self,
        name: str,
        units: UnitSystem | None = None,
        description: str = "",
        author: str = "",
    ) -> ProjectFile:
        """
        Create a new project.

        Args:
            name: Project name
            units: Unit system (defaults to SI)
            description: Optional description
            author: Optional author name

        Returns:
            New ProjectFile instance
        """
        logger.info(f"Creating new project: {name}")

        project = Project(
            name=name,
            units=units or SI_UNITS,
            description=description,
            author=author,
        )

        project_file = ProjectFile(project=project)
        self._current_project = project_file
        self._current_path = None

        logger.info(f"Project created: {project.id}")
        return project_file

    def save_project(self, path: Path | str | None = None) -> Path:
        """
        Save the current project.

        Args:
            path: Destination path (uses current path if None)

        Returns:
            Path where the project was saved

        Raises:
            FileError: If no project is open or save fails
        """
        if self._current_project is None:
            raise FileError("No project is currently open")

        save_path = Path(path) if path else self._current_path
        if save_path is None:
            raise FileError("No save path specified and project has never been saved")

        actual_path = self.file_repository.save(self._current_project, save_path)
        self._current_path = actual_path

        # Update recent projects
        self._add_to_recent(actual_path, self._current_project.project.name)

        logger.info(f"Project saved to {actual_path}")
        return actual_path

    def save_project_as(self, path: Path | str) -> Path:
        """
        Save the current project to a new location.

        Args:
            path: New destination path

        Returns:
            Path where the project was saved
        """
        return self.save_project(path)

    def open_project(self, path: Path | str) -> ProjectFile:
        """
        Open an existing project.

        Args:
            path: Path to the .paz file

        Returns:
            Loaded ProjectFile

        Raises:
            ProjectNotFoundError: If file doesn't exist
            InvalidProjectFileError: If file is corrupted
        """
        logger.info(f"Opening project: {path}")

        project_file = self.file_repository.load(path)
        self._current_project = project_file
        self._current_path = Path(path)

        # Update recent projects
        self._add_to_recent(self._current_path, project_file.project.name)

        logger.info(f"Project opened: {project_file.project.name}")
        return project_file

    def close_project(self) -> None:
        """Close the current project."""
        if self._current_project is not None:
            logger.info(f"Closing project: {self._current_project.project.name}")
        self._current_project = None
        self._current_path = None

    def get_recent_projects(self) -> list[RecentProject]:
        """Get list of recently opened projects."""
        # Filter out projects that no longer exist
        valid_recent = [
            rp for rp in self._recent_projects if Path(rp.path).exists()
        ]
        if len(valid_recent) != len(self._recent_projects):
            self._recent_projects = valid_recent
            self._save_settings()
        return self._recent_projects

    def clear_recent_projects(self) -> None:
        """Clear the recent projects list."""
        self._recent_projects = []
        self._save_settings()

    def _add_to_recent(self, path: Path, name: str) -> None:
        """Add a project to the recent list."""
        path_str = str(path.absolute())

        # Remove if already in list
        self._recent_projects = [
            rp for rp in self._recent_projects if rp.path != path_str
        ]

        # Add at beginning
        self._recent_projects.insert(
            0,
            RecentProject(
                path=path_str,
                name=name,
                opened_at=datetime.now(UTC),
            ),
        )

        # Trim to max size
        self._recent_projects = self._recent_projects[:MAX_RECENT_PROJECTS]

        self._save_settings()

    def _load_settings(self) -> None:
        """Load settings from disk."""
        if not self.settings_path.exists():
            return

        try:
            with self.settings_path.open(encoding="utf-8") as f:
                data = json.load(f)

            self._recent_projects = [
                RecentProject.from_dict(rp) for rp in data.get("recent_projects", [])
            ]
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Failed to load settings: {e}")
            self._recent_projects = []

    def _save_settings(self) -> None:
        """Save settings to disk."""
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "recent_projects": [rp.to_dict() for rp in self._recent_projects],
                "autosave_interval": AUTOSAVE_INTERVAL_SECONDS,
            }

            with self.settings_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            logger.warning(f"Failed to save settings: {e}")

    def get_project_info(self, path: Path | str) -> dict[str, Any]:
        """
        Get basic info about a project without fully loading it.

        Args:
            path: Path to the project file

        Returns:
            Dictionary with project metadata
        """
        project_file = self.file_repository.load(path)
        return project_file.project.to_dict()

    def export_to_json(self, path: Path | str) -> Path:
        """
        Export current project to uncompressed JSON (for debugging).

        Args:
            path: Destination path

        Returns:
            Path where the file was saved
        """
        if self._current_project is None:
            raise FileError("No project is currently open")

        return self.file_repository.save_json(
            self._current_project.to_dict(),
            path,
        )
