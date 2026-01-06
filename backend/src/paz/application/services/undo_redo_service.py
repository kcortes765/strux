"""
Undo/Redo service for command history management.

Provides functionality to execute commands and maintain history
for undo and redo operations.
"""

from paz.application.commands.base_command import Command
from paz.core.constants import MAX_UNDO_LEVELS
from paz.core.logging_config import get_logger


logger = get_logger("undo_redo")


class UndoRedoService:
    """
    Manages command history for undo/redo functionality.

    Maintains two stacks: one for commands that can be undone,
    and one for commands that can be redone.
    """

    def __init__(self, max_history: int = MAX_UNDO_LEVELS) -> None:
        """
        Initialize the undo/redo service.

        Args:
            max_history: Maximum number of commands to keep in history
        """
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []
        self._max_history = max_history

    @property
    def can_undo(self) -> bool:
        """Check if there are commands to undo."""
        return len(self._undo_stack) > 0

    @property
    def can_redo(self) -> bool:
        """Check if there are commands to redo."""
        return len(self._redo_stack) > 0

    @property
    def undo_description(self) -> str | None:
        """Get description of next command to undo."""
        if self._undo_stack:
            return self._undo_stack[-1].description
        return None

    @property
    def redo_description(self) -> str | None:
        """Get description of next command to redo."""
        if self._redo_stack:
            return self._redo_stack[-1].description
        return None

    def execute(self, command: Command) -> object:
        """
        Execute a command and add it to history.

        Args:
            command: The command to execute

        Returns:
            Result of command execution
        """
        result = command.execute()

        # Add to undo stack
        self._undo_stack.append(command)

        # Trim history if needed
        while len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)

        # Clear redo stack (new action invalidates redo history)
        self._redo_stack.clear()

        logger.debug(f"Executed: {command.description}")

        return result

    def undo(self) -> bool:
        """
        Undo the last command.

        Returns:
            True if a command was undone, False if nothing to undo
        """
        if not self._undo_stack:
            return False

        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

        logger.debug(f"Undone: {command.description}")

        return True

    def redo(self) -> bool:
        """
        Redo the last undone command.

        Returns:
            True if a command was redone, False if nothing to redo
        """
        if not self._redo_stack:
            return False

        command = self._redo_stack.pop()
        command.redo()
        self._undo_stack.append(command)

        logger.debug(f"Redone: {command.description}")

        return True

    def clear(self) -> None:
        """Clear all history."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def get_undo_history(self) -> list[str]:
        """Get descriptions of commands that can be undone."""
        return [cmd.description for cmd in reversed(self._undo_stack)]

    def get_redo_history(self) -> list[str]:
        """Get descriptions of commands that can be redone."""
        return [cmd.description for cmd in reversed(self._redo_stack)]

    @property
    def undo_count(self) -> int:
        """Get number of commands that can be undone."""
        return len(self._undo_stack)

    @property
    def redo_count(self) -> int:
        """Get number of commands that can be redone."""
        return len(self._redo_stack)
