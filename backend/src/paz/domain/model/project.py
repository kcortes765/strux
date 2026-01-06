"""
Project model for PAZ.

A Project represents a structural analysis project containing:
- Metadata (name, dates, version)
- Unit system configuration
- Structural model (nodes, frames, materials, sections)
- Load cases and combinations
- Analysis results
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from paz.core.units import SI_UNITS, UnitSystem


@dataclass
class Project:
    """
    Represents a structural analysis project.

    Attributes:
        id: Unique identifier for the project
        name: Human-readable project name
        units: Unit system configuration
        created_at: Timestamp when project was created
        modified_at: Timestamp of last modification
        version: File format version for compatibility
        description: Optional project description
        author: Optional author name
    """

    name: str
    id: UUID = field(default_factory=uuid4)
    units: UnitSystem = field(default_factory=lambda: SI_UNITS)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    modified_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    version: str = "1.0"
    description: str = ""
    author: str = ""

    def touch(self) -> None:
        """Update the modified_at timestamp."""
        self.modified_at = datetime.now(UTC)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize project to dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "units": self.units.to_dict(),
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "version": self.version,
            "description": self.description,
            "author": self.author,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        """
        Create a Project from a dictionary.

        Args:
            data: Dictionary with project data

        Returns:
            New Project instance
        """
        return cls(
            id=UUID(data["id"]) if "id" in data else uuid4(),
            name=data.get("name", "Untitled Project"),
            units=UnitSystem.from_dict(data.get("units", {})),
            created_at=datetime.fromisoformat(data["created_at"])
            if "created_at" in data
            else datetime.now(UTC),
            modified_at=datetime.fromisoformat(data["modified_at"])
            if "modified_at" in data
            else datetime.now(UTC),
            version=data.get("version", "1.0"),
            description=data.get("description", ""),
            author=data.get("author", ""),
        )


@dataclass
class ProjectFile:
    """
    Complete project file structure for serialization.

    This represents the full .paz file format including:
    - Project metadata
    - Structural model data
    - Load definitions
    - Analysis results
    """

    project: Project
    model: dict[str, Any] = field(default_factory=dict)
    load_cases: list[dict[str, Any]] = field(default_factory=list)
    load_combinations: list[dict[str, Any]] = field(default_factory=list)
    results: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for JSON export."""
        return {
            "version": self.project.version,
            "project": self.project.to_dict(),
            "model": self.model,
            "load_cases": self.load_cases,
            "load_combinations": self.load_combinations,
            "results": self.results,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectFile":
        """Create from dictionary."""
        return cls(
            project=Project.from_dict(data.get("project", {})),
            model=data.get("model", {}),
            load_cases=data.get("load_cases", []),
            load_combinations=data.get("load_combinations", []),
            results=data.get("results", {}),
        )
