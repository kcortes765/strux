"""
Commands for node operations.

Implements reversible commands for creating, deleting, and modifying nodes.
"""

from dataclasses import dataclass

from paz.application.commands.base_command import Command
from paz.domain.model.node import Node
from paz.domain.model.restraint import Restraint
from paz.domain.model.structural_model import StructuralModel


@dataclass
class CreateNodeCommand(Command):
    """Command to create a new node."""

    model: StructuralModel
    x: float
    y: float
    z: float
    restraint: Restraint | None = None
    node_id: int | None = None
    _created_node: Node | None = None

    def execute(self) -> Node:
        """Create the node and return it."""
        self._created_node = self.model.add_node(
            x=self.x,
            y=self.y,
            z=self.z,
            restraint=self.restraint,
            node_id=self.node_id,
        )
        return self._created_node

    def undo(self) -> None:
        """Remove the created node."""
        if self._created_node is not None:
            self.model.remove_node(self._created_node.id)
            self._created_node = None

    @property
    def description(self) -> str:
        return f"Create node at ({self.x}, {self.y}, {self.z})"


@dataclass
class DeleteNodeCommand(Command):
    """Command to delete a node."""

    model: StructuralModel
    node_id: int
    _deleted_node: Node | None = None

    def execute(self) -> None:
        """Delete the node."""
        self._deleted_node = self.model.remove_node(self.node_id)

    def undo(self) -> None:
        """Restore the deleted node."""
        if self._deleted_node is not None:
            self.model.add_node(
                x=self._deleted_node.x,
                y=self._deleted_node.y,
                z=self._deleted_node.z,
                restraint=self._deleted_node.restraint,
                node_id=self._deleted_node.id,
                check_duplicate=False,
            )
            self._deleted_node = None

    @property
    def description(self) -> str:
        return f"Delete node {self.node_id}"


@dataclass
class MoveNodeCommand(Command):
    """Command to move a node to new coordinates."""

    model: StructuralModel
    node_id: int
    new_x: float
    new_y: float
    new_z: float
    _old_x: float | None = None
    _old_y: float | None = None
    _old_z: float | None = None

    def execute(self) -> Node:
        """Move the node and return it."""
        node = self.model.get_node(self.node_id)

        # Store old position for undo
        self._old_x = node.x
        self._old_y = node.y
        self._old_z = node.z

        # Move to new position
        node.move_to(self.new_x, self.new_y, self.new_z)

        return node

    def undo(self) -> None:
        """Restore the node to its original position."""
        if self._old_x is not None:
            node = self.model.get_node(self.node_id)
            node.move_to(self._old_x, self._old_y, self._old_z)  # type: ignore[arg-type]

    @property
    def description(self) -> str:
        return f"Move node {self.node_id} to ({self.new_x}, {self.new_y}, {self.new_z})"


@dataclass
class UpdateNodeRestraintCommand(Command):
    """Command to update node restraints."""

    model: StructuralModel
    node_id: int
    new_restraint: Restraint
    _old_restraint: Restraint | None = None

    def execute(self) -> Node:
        """Update the restraint and return the node."""
        node = self.model.get_node(self.node_id)

        # Store old restraint for undo
        self._old_restraint = node.restraint

        # Update restraint
        node.restraint = self.new_restraint

        return node

    def undo(self) -> None:
        """Restore the original restraint."""
        if self._old_restraint is not None:
            node = self.model.get_node(self.node_id)
            node.restraint = self._old_restraint

    @property
    def description(self) -> str:
        return f"Update restraint for node {self.node_id}"


@dataclass
class MoveNodeByOffsetCommand(Command):
    """Command to move a node by an offset."""

    model: StructuralModel
    node_id: int
    dx: float
    dy: float
    dz: float

    def execute(self) -> Node:
        """Move the node by offset."""
        node = self.model.get_node(self.node_id)
        node.move_by(self.dx, self.dy, self.dz)
        return node

    def undo(self) -> None:
        """Move the node back."""
        node = self.model.get_node(self.node_id)
        node.move_by(-self.dx, -self.dy, -self.dz)

    @property
    def description(self) -> str:
        return f"Move node {self.node_id} by ({self.dx}, {self.dy}, {self.dz})"
