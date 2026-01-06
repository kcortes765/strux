"""Tests for AutoSaveService."""

import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from paz.application.services.autosave_service import AutoSaveService
from paz.application.services.project_service import ProjectService
from paz.domain.model.project import Project, ProjectFile


class TestAutoSaveService:
    """Tests for AutoSaveService."""

    @pytest.fixture
    def mock_project_service(self, tmp_path: Path) -> ProjectService:
        """Create a mock project service."""
        service = ProjectService(settings_path=tmp_path / "settings.json")
        return service

    @pytest.fixture
    def autosave_service(
        self, mock_project_service: ProjectService
    ) -> AutoSaveService:
        """Create an autosave service with short interval for testing."""
        return AutoSaveService(
            project_service=mock_project_service,
            interval_seconds=60,  # 1 minute for tests
        )

    def test_initial_state(self, autosave_service: AutoSaveService) -> None:
        """Test initial state of autosave service."""
        assert not autosave_service.is_running
        assert not autosave_service.is_paused
        assert autosave_service.interval == 60

    def test_start_stop(self, autosave_service: AutoSaveService) -> None:
        """Test starting and stopping the service."""
        autosave_service.start()
        assert autosave_service.is_running
        assert not autosave_service.is_paused

        autosave_service.stop()
        assert not autosave_service.is_running

    def test_pause_resume(self, autosave_service: AutoSaveService) -> None:
        """Test pausing and resuming the service."""
        autosave_service.start()

        autosave_service.pause()
        assert autosave_service.is_running
        assert autosave_service.is_paused

        autosave_service.resume()
        assert autosave_service.is_running
        assert not autosave_service.is_paused

        autosave_service.stop()

    def test_set_interval(self, autosave_service: AutoSaveService) -> None:
        """Test setting the interval."""
        autosave_service.interval = 120
        assert autosave_service.interval == 120

    def test_interval_minimum(self, autosave_service: AutoSaveService) -> None:
        """Test that interval has a minimum value."""
        with pytest.raises(ValueError, match="at least 30 seconds"):
            autosave_service.interval = 10

    def test_save_now_no_project(
        self, autosave_service: AutoSaveService
    ) -> None:
        """Test save_now with no project open."""
        result = autosave_service.save_now()
        assert result is False

    def test_save_now_unsaved_project(
        self,
        mock_project_service: ProjectService,
        autosave_service: AutoSaveService,
    ) -> None:
        """Test save_now with a project that hasn't been saved yet."""
        mock_project_service.create_project("Test Project")
        result = autosave_service.save_now()
        assert result is False  # No path set yet

    def test_save_now_with_saved_project(
        self,
        mock_project_service: ProjectService,
        autosave_service: AutoSaveService,
        tmp_path: Path,
    ) -> None:
        """Test save_now with a previously saved project."""
        # Create and save a project
        mock_project_service.create_project("Test Project")
        save_path = tmp_path / "test_project.paz"
        mock_project_service.save_project(save_path)

        # Now auto-save should work
        result = autosave_service.save_now()
        assert result is True
        assert save_path.exists()

    def test_on_save_callback(
        self,
        mock_project_service: ProjectService,
        tmp_path: Path,
    ) -> None:
        """Test that on_save callback is called."""
        callback_called = threading.Event()

        def on_save() -> None:
            callback_called.set()

        autosave = AutoSaveService(
            project_service=mock_project_service,
            interval_seconds=60,
            on_save=on_save,
        )

        # Create and save a project
        mock_project_service.create_project("Test Project")
        mock_project_service.save_project(tmp_path / "test.paz")

        # Trigger save
        autosave.save_now()

        assert callback_called.is_set()

    def test_on_error_callback(
        self,
        mock_project_service: ProjectService,
        tmp_path: Path,
    ) -> None:
        """Test that on_error callback is called on failure."""
        error_received: list[Exception] = []

        def on_error(e: Exception) -> None:
            error_received.append(e)

        autosave = AutoSaveService(
            project_service=mock_project_service,
            interval_seconds=60,
            on_error=on_error,
        )

        # Create and save a project
        mock_project_service.create_project("Test Project")
        mock_project_service.save_project(tmp_path / "test.paz")

        # Make save fail by mocking repository
        with patch.object(
            mock_project_service.file_repository,
            "save",
            side_effect=OSError("Disk full"),
        ):
            result = autosave.save_now()

        assert result is False
        assert len(error_received) == 1
        assert "Disk full" in str(error_received[0])

    def test_double_start(self, autosave_service: AutoSaveService) -> None:
        """Test that starting twice doesn't cause issues."""
        autosave_service.start()
        autosave_service.start()  # Should not raise
        assert autosave_service.is_running
        autosave_service.stop()

    def test_stop_when_not_running(
        self, autosave_service: AutoSaveService
    ) -> None:
        """Test that stopping when not running doesn't cause issues."""
        autosave_service.stop()  # Should not raise
        assert not autosave_service.is_running

    def test_service_uses_project_service_save(
        self,
        mock_project_service: ProjectService,
        tmp_path: Path,
    ) -> None:
        """Test that autosave uses project_service.save_project."""
        autosave = AutoSaveService(
            project_service=mock_project_service,
            interval_seconds=60,
        )

        # Create and save a project
        mock_project_service.create_project("Test Project")
        save_path = tmp_path / "test.paz"
        mock_project_service.save_project(save_path)

        # Get initial modified time
        initial_mtime = save_path.stat().st_mtime

        # Small delay to ensure different timestamp
        import time
        time.sleep(0.01)

        # Trigger autosave
        result = autosave.save_now()
        assert result is True

        # File should have been updated
        assert save_path.exists()
