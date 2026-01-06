"""Tests for FileRepository."""

import pytest
from pathlib import Path

from paz.core.exceptions import ProjectNotFoundError, InvalidProjectFileError
from paz.domain.model.project import Project, ProjectFile
from paz.infrastructure.repositories.file_repository import FileRepository


class TestFileRepository:
    """Tests for FileRepository."""

    @pytest.fixture
    def repo(self, tmp_path: Path) -> FileRepository:
        """Create a file repository with a temp directory."""
        return FileRepository(base_path=tmp_path)

    @pytest.fixture
    def sample_project_file(self) -> ProjectFile:
        """Create a sample project file."""
        project = Project(
            name="Test Project",
            description="A test project",
            author="Tester",
        )
        return ProjectFile(
            project=project,
            model={"nodes": [{"id": 1, "x": 0, "y": 0, "z": 0}]},
            load_cases=[{"id": 1, "name": "Dead", "type": "Dead"}],
        )

    def test_save_creates_file(
        self, repo: FileRepository, sample_project_file: ProjectFile, tmp_path: Path
    ) -> None:
        """Saving should create a .paz file."""
        path = repo.save(sample_project_file, "test_project.paz")

        assert path.exists()
        assert path.suffix == ".paz"

    def test_save_adds_extension_if_missing(
        self, repo: FileRepository, sample_project_file: ProjectFile
    ) -> None:
        """Saving without .paz extension should add it."""
        path = repo.save(sample_project_file, "test_project")

        assert path.suffix == ".paz"

    def test_save_creates_parent_directories(
        self, repo: FileRepository, sample_project_file: ProjectFile, tmp_path: Path
    ) -> None:
        """Saving to nested path should create directories."""
        path = repo.save(sample_project_file, "subdir/nested/project.paz")

        assert path.exists()
        assert path.parent.name == "nested"

    def test_load_returns_project_file(
        self, repo: FileRepository, sample_project_file: ProjectFile
    ) -> None:
        """Loading should return a ProjectFile with correct data."""
        save_path = repo.save(sample_project_file, "test.paz")
        loaded = repo.load(save_path)

        assert loaded.project.name == "Test Project"
        assert loaded.project.description == "A test project"
        assert len(loaded.model["nodes"]) == 1

    def test_load_nonexistent_raises_error(self, repo: FileRepository) -> None:
        """Loading nonexistent file should raise ProjectNotFoundError."""
        with pytest.raises(ProjectNotFoundError):
            repo.load("nonexistent.paz")

    def test_save_load_roundtrip(
        self, repo: FileRepository, sample_project_file: ProjectFile
    ) -> None:
        """Save and load should preserve all data."""
        save_path = repo.save(sample_project_file, "roundtrip.paz")
        loaded = repo.load(save_path)

        assert loaded.project.name == sample_project_file.project.name
        assert loaded.model == sample_project_file.model
        assert loaded.load_cases == sample_project_file.load_cases

    def test_exists_returns_true_for_existing(
        self, repo: FileRepository, sample_project_file: ProjectFile
    ) -> None:
        """exists() should return True for existing files."""
        repo.save(sample_project_file, "exists.paz")
        assert repo.exists("exists.paz")

    def test_exists_returns_false_for_missing(self, repo: FileRepository) -> None:
        """exists() should return False for missing files."""
        assert not repo.exists("missing.paz")

    def test_delete_removes_file(
        self, repo: FileRepository, sample_project_file: ProjectFile
    ) -> None:
        """delete() should remove the file."""
        path = repo.save(sample_project_file, "to_delete.paz")
        assert path.exists()

        result = repo.delete("to_delete.paz")

        assert result is True
        assert not path.exists()

    def test_delete_returns_false_for_missing(self, repo: FileRepository) -> None:
        """delete() should return False for missing files."""
        result = repo.delete("missing.paz")
        assert result is False

    def test_file_is_gzip_compressed(
        self, repo: FileRepository, sample_project_file: ProjectFile, tmp_path: Path
    ) -> None:
        """Saved file should be gzip compressed."""
        path = repo.save(sample_project_file, "compressed.paz")

        # Gzip files start with magic bytes 1f 8b
        with open(path, "rb") as f:
            magic = f.read(2)

        assert magic == b"\x1f\x8b"

    def test_save_json_creates_uncompressed(
        self, repo: FileRepository, tmp_path: Path
    ) -> None:
        """save_json should create uncompressed JSON."""
        data = {"test": "data", "number": 42}
        path = repo.save_json(data, "debug.json")

        assert path.exists()
        loaded = repo.load_json(path)
        assert loaded == data
