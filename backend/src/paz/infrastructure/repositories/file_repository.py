"""
File repository for PAZ projects.

Handles saving and loading project files in .paz format.
The .paz format is JSON compressed with gzip.
"""

import gzip
import json
from pathlib import Path
from typing import Any

from paz.core.constants import PAZ_FILE_EXTENSION, PAZ_FILE_VERSION
from paz.core.exceptions import FileError, InvalidProjectFileError, ProjectNotFoundError
from paz.core.logging_config import get_logger
from paz.domain.model.project import ProjectFile


logger = get_logger("file_repository")


class FileRepository:
    """
    Repository for saving and loading project files.

    The .paz format is a gzip-compressed JSON file containing:
    - Project metadata
    - Structural model
    - Load cases and combinations
    - Analysis results (optional)
    """

    def __init__(self, base_path: Path | None = None) -> None:
        """
        Initialize the file repository.

        Args:
            base_path: Optional base directory for relative paths.
                      Defaults to current working directory.
        """
        self.base_path = base_path or Path.cwd()

    def _resolve_path(self, path: Path | str) -> Path:
        """Resolve a path, making it absolute if necessary."""
        p = Path(path)
        if not p.is_absolute():
            p = self.base_path / p
        return p

    def _ensure_extension(self, path: Path) -> Path:
        """Ensure the path has the .paz extension."""
        if path.suffix.lower() != PAZ_FILE_EXTENSION:
            return path.with_suffix(PAZ_FILE_EXTENSION)
        return path

    def save(self, project_file: ProjectFile, path: Path | str) -> Path:
        """
        Save a project file to disk.

        Args:
            project_file: The project file to save
            path: Destination path (will add .paz extension if missing)

        Returns:
            The actual path where the file was saved

        Raises:
            FileError: If the file cannot be written
        """
        resolved_path = self._ensure_extension(self._resolve_path(path))

        logger.info(f"Saving project to {resolved_path}")

        try:
            # Ensure parent directory exists
            resolved_path.parent.mkdir(parents=True, exist_ok=True)

            # Update modified timestamp
            project_file.project.touch()

            # Serialize to JSON
            data = project_file.to_dict()
            json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

            # Compress and write
            with gzip.open(resolved_path, "wb") as f:
                f.write(json_bytes)

            logger.info(
                f"Project saved successfully: {resolved_path} "
                f"({len(json_bytes)} bytes -> {resolved_path.stat().st_size} bytes)"
            )

            return resolved_path

        except OSError as e:
            logger.error(f"Failed to save project: {e}")
            raise FileError(
                f"Failed to save project: {e}",
                path=str(resolved_path),
            ) from e

    def load(self, path: Path | str) -> ProjectFile:
        """
        Load a project file from disk.

        Args:
            path: Path to the .paz file

        Returns:
            Loaded ProjectFile instance

        Raises:
            ProjectNotFoundError: If the file doesn't exist
            InvalidProjectFileError: If the file is corrupted or invalid
        """
        resolved_path = self._resolve_path(path)

        logger.info(f"Loading project from {resolved_path}")

        if not resolved_path.exists():
            raise ProjectNotFoundError(str(resolved_path))

        try:
            # Read and decompress
            with gzip.open(resolved_path, "rb") as f:
                json_bytes = f.read()

            # Parse JSON
            data = json.loads(json_bytes.decode("utf-8"))

            # Validate version
            file_version = data.get("version", "unknown")
            if not self._is_version_compatible(file_version):
                logger.warning(
                    f"Project file version {file_version} may not be fully compatible "
                    f"with current version {PAZ_FILE_VERSION}"
                )

            # Deserialize
            project_file = ProjectFile.from_dict(data)

            logger.info(
                f"Project loaded successfully: {project_file.project.name} "
                f"(version {file_version})"
            )

            return project_file

        except gzip.BadGzipFile as e:
            logger.error(f"Invalid gzip file: {e}")
            raise InvalidProjectFileError(
                str(resolved_path),
                reason="File is not a valid gzip archive",
            ) from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            raise InvalidProjectFileError(
                str(resolved_path),
                reason=f"Invalid JSON: {e}",
            ) from e
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Invalid project structure: {e}")
            raise InvalidProjectFileError(
                str(resolved_path),
                reason=f"Invalid project structure: {e}",
            ) from e

    def _is_version_compatible(self, file_version: str) -> bool:
        """Check if a file version is compatible with current version."""
        try:
            file_major = int(file_version.split(".")[0])
            current_major = int(PAZ_FILE_VERSION.split(".")[0])
            return file_major == current_major
        except (ValueError, IndexError):
            return False

    def exists(self, path: Path | str) -> bool:
        """Check if a project file exists."""
        return self._resolve_path(path).exists()

    def delete(self, path: Path | str) -> bool:
        """
        Delete a project file.

        Args:
            path: Path to the file to delete

        Returns:
            True if file was deleted, False if it didn't exist

        Raises:
            FileError: If deletion fails
        """
        resolved_path = self._resolve_path(path)

        if not resolved_path.exists():
            return False

        try:
            resolved_path.unlink()
            logger.info(f"Deleted project file: {resolved_path}")
            return True
        except OSError as e:
            raise FileError(
                f"Failed to delete project: {e}",
                path=str(resolved_path),
            ) from e

    def save_json(self, data: dict[str, Any], path: Path | str) -> Path:
        """
        Save data as uncompressed JSON (for debugging/export).

        Args:
            data: Dictionary to save
            path: Destination path

        Returns:
            The actual path where the file was saved
        """
        resolved_path = self._resolve_path(path)
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        with resolved_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return resolved_path

    def load_json(self, path: Path | str) -> dict[str, Any]:
        """
        Load data from uncompressed JSON file.

        Args:
            path: Path to JSON file

        Returns:
            Loaded dictionary
        """
        resolved_path = self._resolve_path(path)

        if not resolved_path.exists():
            raise ProjectNotFoundError(str(resolved_path))

        with resolved_path.open(encoding="utf-8") as f:
            return json.load(f)  # type: ignore[no-any-return]
