"""
Base command for implementing the Command pattern.

Commands are reversible operations that support undo/redo.
"""

from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Abstract base class for reversible commands.

    All model-modifying operations should be implemented as commands
    to support undo/redo functionality.
    """

    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the command.

        Returns:
            Result of the command execution (type depends on command)
        """
        pass

    @abstractmethod
    def undo(self) -> None:
        """Reverse the command effects."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of the command."""
        pass

    def redo(self) -> Any:
        """
        Re-execute the command.

        Default implementation just calls execute().
        Override if redo behavior should differ.

        Returns:
            Result of the command execution
        """
        return self.execute()


class CompositeCommand(Command):
    """
    A command that groups multiple commands together.

    Useful for operations that consist of multiple steps.
    """

    def __init__(self, commands: list[Command], description: str = "") -> None:
        self._commands = commands
        self._description = description or f"Composite ({len(commands)} commands)"
        self._executed_commands: list[Command] = []

    def execute(self) -> list[Any]:
        """Execute all commands in order."""
        results = []
        self._executed_commands = []

        for cmd in self._commands:
            result = cmd.execute()
            results.append(result)
            self._executed_commands.append(cmd)

        return results

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for cmd in reversed(self._executed_commands):
            cmd.undo()
        self._executed_commands = []

    @property
    def description(self) -> str:
        return self._description
