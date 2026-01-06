"""Integration tests for project save/load roundtrip."""

import pytest
from pathlib import Path

from paz.core.units import IMPERIAL_UNITS, SI_UNITS
from paz.domain.model.project import Project, ProjectFile
from paz.application.services.project_service import ProjectService
from paz.infrastructure.repositories.file_repository import FileRepository


class TestProjectServiceRoundtrip:
    """Integration tests for ProjectService save/load operations."""

    @pytest.fixture
    def project_service(self, tmp_path: Path) -> ProjectService:
        """Create a project service with temp directories."""
        repo = FileRepository(base_path=tmp_path)
        settings_path = tmp_path / "settings.json"
        return ProjectService(file_repository=repo, settings_path=settings_path)

    def test_create_save_open_cycle(
        self, project_service: ProjectService, tmp_path: Path
    ) -> None:
        """Create, save, and reopen a project."""
        # Create
        project_file = project_service.create_project(
            name="Integration Test",
            units=IMPERIAL_UNITS,
            description="Testing the full cycle",
            author="Integration Tester",
        )

        assert project_service.current_project is not None
        assert project_service.current_project.project.name == "Integration Test"

        # Save
        save_path = project_service.save_project(tmp_path / "integration.paz")
        assert save_path.exists()

        # Close
        project_service.close_project()
        assert project_service.current_project is None

        # Reopen
        reopened = project_service.open_project(save_path)

        assert reopened.project.name == "Integration Test"
        assert reopened.project.units == IMPERIAL_UNITS
        assert reopened.project.description == "Testing the full cycle"

    def test_save_as_creates_new_file(
        self, project_service: ProjectService, tmp_path: Path
    ) -> None:
        """Save As should create a new file without affecting original."""
        # Create and save
        project_service.create_project(name="Original")
        original_path = project_service.save_project(tmp_path / "original.paz")

        # Save As
        new_path = project_service.save_project_as(tmp_path / "copy.paz")

        assert original_path.exists()
        assert new_path.exists()
        assert original_path != new_path

    def test_recent_projects_updated_on_open(
        self, project_service: ProjectService, tmp_path: Path
    ) -> None:
        """Opening a project should add it to recent list."""
        # Create and save multiple projects
        project_service.create_project(name="Project 1")
        path1 = project_service.save_project(tmp_path / "project1.paz")

        project_service.create_project(name="Project 2")
        path2 = project_service.save_project(tmp_path / "project2.paz")

        # Check recent projects
        recent = project_service.get_recent_projects()

        assert len(recent) == 2
        assert recent[0].name == "Project 2"  # Most recent first
        assert recent[1].name == "Project 1"

    def test_recent_projects_persisted(self, tmp_path: Path) -> None:
        """Recent projects should persist across service instances."""
        settings_path = tmp_path / "settings.json"
        repo = FileRepository(base_path=tmp_path)

        # First service instance
        service1 = ProjectService(file_repository=repo, settings_path=settings_path)
        service1.create_project(name="Persisted Project")
        service1.save_project(tmp_path / "persisted.paz")

        # New service instance (simulating app restart)
        service2 = ProjectService(file_repository=repo, settings_path=settings_path)
        recent = service2.get_recent_projects()

        assert len(recent) == 1
        assert recent[0].name == "Persisted Project"

    def test_full_project_data_roundtrip(
        self, project_service: ProjectService, tmp_path: Path
    ) -> None:
        """All project data should survive save/load cycle."""
        # Create project with model data
        project_file = project_service.create_project(
            name="Full Data Test",
            units=SI_UNITS,
        )

        # Add model data
        project_file.model = {
            "nodes": [
                {"id": 1, "x": 0.0, "y": 0.0, "z": 0.0},
                {"id": 2, "x": 5.0, "y": 0.0, "z": 0.0},
                {"id": 3, "x": 5.0, "y": 0.0, "z": 3.0},
            ],
            "frames": [
                {"id": 1, "node_i": 1, "node_j": 2},
                {"id": 2, "node_i": 2, "node_j": 3},
            ],
        }
        project_file.load_cases = [
            {"id": 1, "name": "Dead", "type": "Dead"},
            {"id": 2, "name": "Live", "type": "Live"},
        ]

        # Save and reopen
        save_path = project_service.save_project(tmp_path / "full_data.paz")
        project_service.close_project()
        reopened = project_service.open_project(save_path)

        # Verify all data
        assert len(reopened.model["nodes"]) == 3
        assert len(reopened.model["frames"]) == 2
        assert len(reopened.load_cases) == 2
        assert reopened.model["nodes"][2]["z"] == 3.0
