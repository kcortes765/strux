"""Tests for Project model."""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from paz.core.units import UnitSystem, LengthUnit, ForceUnit, IMPERIAL_UNITS
from paz.domain.model.project import Project, ProjectFile


class TestProject:
    """Tests for Project dataclass."""

    def test_create_project_with_name(self) -> None:
        """Create a project with just a name."""
        project = Project(name="Test Project")

        assert project.name == "Test Project"
        assert isinstance(project.id, UUID)
        assert project.units.length == LengthUnit.METER
        assert project.version == "1.0"

    def test_create_project_with_units(self) -> None:
        """Create a project with custom units."""
        project = Project(
            name="Imperial Project",
            units=IMPERIAL_UNITS,
        )

        assert project.units.length == LengthUnit.FOOT
        assert project.units.force == ForceUnit.KIP

    def test_project_touch_updates_modified_at(self) -> None:
        """Calling touch() should update modified_at."""
        project = Project(name="Test")
        original_modified = project.modified_at

        # Small delay to ensure time difference
        import time

        time.sleep(0.01)

        project.touch()

        assert project.modified_at > original_modified

    def test_project_to_dict(self) -> None:
        """Project should serialize to dict correctly."""
        project = Project(
            name="Test Project",
            description="A test",
            author="Tester",
        )

        data = project.to_dict()

        assert data["name"] == "Test Project"
        assert data["description"] == "A test"
        assert data["author"] == "Tester"
        assert "id" in data
        assert "created_at" in data
        assert "modified_at" in data
        assert data["units"]["length"] == "m"

    def test_project_from_dict(self) -> None:
        """Project should deserialize from dict correctly."""
        data = {
            "id": "12345678-1234-1234-1234-123456789012",
            "name": "Loaded Project",
            "units": {"length": "ft", "force": "kip", "angle": "deg"},
            "created_at": "2024-01-01T00:00:00+00:00",
            "modified_at": "2024-01-02T00:00:00+00:00",
            "version": "1.0",
            "description": "Loaded",
            "author": "Someone",
        }

        project = Project.from_dict(data)

        assert project.name == "Loaded Project"
        assert str(project.id) == "12345678-1234-1234-1234-123456789012"
        assert project.units.length == LengthUnit.FOOT
        assert project.description == "Loaded"

    def test_project_roundtrip(self) -> None:
        """Serializing and deserializing should preserve data."""
        original = Project(
            name="Roundtrip Test",
            units=IMPERIAL_UNITS,
            description="Testing roundtrip",
            author="Test Author",
        )

        data = original.to_dict()
        restored = Project.from_dict(data)

        assert restored.name == original.name
        assert str(restored.id) == str(original.id)
        assert restored.units == original.units
        assert restored.description == original.description
        assert restored.author == original.author


class TestProjectFile:
    """Tests for ProjectFile dataclass."""

    def test_create_empty_project_file(self) -> None:
        """Create a project file with default empty model."""
        project = Project(name="Test")
        project_file = ProjectFile(project=project)

        assert project_file.project.name == "Test"
        assert project_file.model == {}
        assert project_file.load_cases == []
        assert project_file.load_combinations == []
        assert project_file.results == {}

    def test_project_file_to_dict(self) -> None:
        """ProjectFile should serialize correctly."""
        project = Project(name="Full Test")
        project_file = ProjectFile(
            project=project,
            model={"nodes": [], "frames": []},
            load_cases=[{"id": 1, "name": "Dead"}],
        )

        data = project_file.to_dict()

        assert data["project"]["name"] == "Full Test"
        assert data["model"]["nodes"] == []
        assert len(data["load_cases"]) == 1

    def test_project_file_roundtrip(self) -> None:
        """ProjectFile serialization roundtrip should preserve data."""
        project = Project(name="Roundtrip")
        original = ProjectFile(
            project=project,
            model={"nodes": [{"id": 1, "x": 0}]},
            load_cases=[{"id": 1, "name": "Live"}],
        )

        data = original.to_dict()
        restored = ProjectFile.from_dict(data)

        assert restored.project.name == original.project.name
        assert restored.model == original.model
        assert restored.load_cases == original.load_cases
