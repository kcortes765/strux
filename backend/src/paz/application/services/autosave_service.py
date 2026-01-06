"""
Auto-save service for PAZ projects.

Provides automatic periodic saving of projects to prevent data loss.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from paz.core.constants import AUTOSAVE_INTERVAL_SECONDS
from paz.core.logging_config import get_logger


if TYPE_CHECKING:
    from collections.abc import Callable

    from paz.application.services.project_service import ProjectService


logger = get_logger("autosave_service")


class AutoSaveService:
    """
    Service for automatic periodic saving of projects.

    Features:
    - Configurable save interval (default 5 minutes)
    - Saves to backup file to prevent corruption
    - Can be started/stopped/paused
    - Thread-safe operation

    Example:
        service = ProjectService()
        autosave = AutoSaveService(service)
        autosave.start()
        # ... work with project ...
        autosave.stop()
    """

    def __init__(
        self,
        project_service: ProjectService,
        interval_seconds: int = AUTOSAVE_INTERVAL_SECONDS,
        on_save: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> None:
        """
        Initialize the auto-save service.

        Args:
            project_service: The project service to use for saving
            interval_seconds: Seconds between auto-saves (default: 300 = 5 min)
            on_save: Optional callback called after each successful save
            on_error: Optional callback called on save errors
        """
        self._project_service = project_service
        self._interval = interval_seconds
        self._on_save = on_save
        self._on_error = on_error
        self._timer: threading.Timer | None = None
        self._running = False
        self._paused = False
        self._lock = threading.Lock()

    @property
    def is_running(self) -> bool:
        """Check if auto-save is currently running."""
        return self._running

    @property
    def is_paused(self) -> bool:
        """Check if auto-save is paused."""
        return self._paused

    @property
    def interval(self) -> int:
        """Get the current auto-save interval in seconds."""
        return self._interval

    @interval.setter
    def interval(self, seconds: int) -> None:
        """
        Set the auto-save interval.

        Args:
            seconds: New interval in seconds (minimum 30)
        """
        if seconds < 30:
            raise ValueError("Auto-save interval must be at least 30 seconds")
        self._interval = seconds
        # Restart timer with new interval if running
        if self._running and not self._paused:
            self._restart_timer()

    def start(self) -> None:
        """Start the auto-save timer."""
        with self._lock:
            if self._running:
                logger.warning("AutoSave is already running")
                return

            self._running = True
            self._paused = False
            self._schedule_next_save()
            logger.info(f"AutoSave started (interval: {self._interval}s)")

    def stop(self) -> None:
        """Stop the auto-save timer."""
        with self._lock:
            if not self._running:
                return

            self._running = False
            self._paused = False
            self._cancel_timer()
            logger.info("AutoSave stopped")

    def pause(self) -> None:
        """Pause the auto-save timer."""
        with self._lock:
            if not self._running or self._paused:
                return

            self._paused = True
            self._cancel_timer()
            logger.info("AutoSave paused")

    def resume(self) -> None:
        """Resume the auto-save timer."""
        with self._lock:
            if not self._running or not self._paused:
                return

            self._paused = False
            self._schedule_next_save()
            logger.info("AutoSave resumed")

    def save_now(self) -> bool:
        """
        Trigger an immediate save.

        Returns:
            True if save was successful, False otherwise
        """
        return self._do_save()

    def _schedule_next_save(self) -> None:
        """Schedule the next auto-save."""
        self._cancel_timer()
        self._timer = threading.Timer(self._interval, self._on_timer)
        self._timer.daemon = True
        self._timer.start()

    def _cancel_timer(self) -> None:
        """Cancel the current timer if active."""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _restart_timer(self) -> None:
        """Restart the timer with current interval."""
        self._cancel_timer()
        self._schedule_next_save()

    def _on_timer(self) -> None:
        """Timer callback - performs the auto-save."""
        with self._lock:
            if not self._running or self._paused:
                return

            self._do_save()

            # Schedule next save
            if self._running and not self._paused:
                self._schedule_next_save()

    def _do_save(self) -> bool:
        """
        Perform the actual save operation.

        Returns:
            True if save was successful
        """
        project_service = self._project_service

        # Check if there's a project to save
        if project_service.current_project is None:
            logger.debug("AutoSave: No project open, skipping")
            return False

        # Check if project has been saved before
        if project_service.current_path is None:
            logger.debug("AutoSave: Project not yet saved, skipping")
            return False

        try:
            # Save directly to the current path
            project_service.save_project()

            logger.info(f"AutoSave completed: {project_service.current_path}")

            if self._on_save:
                self._on_save()

            return True

        except Exception as e:
            logger.error(f"AutoSave failed: {e}")
            if self._on_error:
                self._on_error(e)
            return False
