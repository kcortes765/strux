"""Tests for node commands and undo/redo."""

import pytest

from paz.application.commands.node_commands import (
    CreateNodeCommand,
    DeleteNodeCommand,
    MoveNodeCommand,
    UpdateNodeRestraintCommand,
    MoveNodeByOffsetCommand,
)
from paz.application.services.undo_redo_service import UndoRedoService
from paz.domain.model.restraint import FIXED, PINNED, FREE
from paz.domain.model.structural_model import StructuralModel


class TestCreateNodeCommand:
    """Tests for CreateNodeCommand."""

    def test_execute_creates_node(self) -> None:
        """Execute should create a node."""
        model = StructuralModel()
        cmd = CreateNodeCommand(model=model, x=1, y=2, z=3)
        node = cmd.execute()

        assert model.node_count == 1
        assert node.position == (1, 2, 3)

    def test_undo_removes_node(self) -> None:
        """Undo should remove the created node."""
        model = StructuralModel()
        cmd = CreateNodeCommand(model=model, x=1, y=2, z=3)
        cmd.execute()
        cmd.undo()

        assert model.node_count == 0

    def test_execute_with_restraint(self) -> None:
        """Execute should apply restraint."""
        model = StructuralModel()
        cmd = CreateNodeCommand(model=model, x=0, y=0, z=0, restraint=FIXED)
        node = cmd.execute()

        assert node.restraint.is_fixed


class TestDeleteNodeCommand:
    """Tests for DeleteNodeCommand."""

    def test_execute_deletes_node(self) -> None:
        """Execute should delete the node."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)

        cmd = DeleteNodeCommand(model=model, node_id=node.id)
        cmd.execute()

        assert model.node_count == 0

    def test_undo_restores_node(self) -> None:
        """Undo should restore the deleted node."""
        model = StructuralModel()
        node = model.add_node(x=1, y=2, z=3, restraint=PINNED)
        node_id = node.id

        cmd = DeleteNodeCommand(model=model, node_id=node_id)
        cmd.execute()
        cmd.undo()

        assert model.node_count == 1
        restored = model.get_node(node_id)
        assert restored.position == (1, 2, 3)
        assert restored.restraint.is_pinned


class TestMoveNodeCommand:
    """Tests for MoveNodeCommand."""

    def test_execute_moves_node(self) -> None:
        """Execute should move the node."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)

        cmd = MoveNodeCommand(
            model=model, node_id=node.id, new_x=5, new_y=6, new_z=7
        )
        cmd.execute()

        assert node.position == (5, 6, 7)

    def test_undo_restores_position(self) -> None:
        """Undo should restore original position."""
        model = StructuralModel()
        node = model.add_node(x=1, y=2, z=3)

        cmd = MoveNodeCommand(
            model=model, node_id=node.id, new_x=10, new_y=20, new_z=30
        )
        cmd.execute()
        cmd.undo()

        assert node.position == (1, 2, 3)


class TestUpdateNodeRestraintCommand:
    """Tests for UpdateNodeRestraintCommand."""

    def test_execute_updates_restraint(self) -> None:
        """Execute should update restraint."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)

        cmd = UpdateNodeRestraintCommand(
            model=model, node_id=node.id, new_restraint=FIXED
        )
        cmd.execute()

        assert node.restraint.is_fixed

    def test_undo_restores_restraint(self) -> None:
        """Undo should restore original restraint."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0, restraint=PINNED)

        cmd = UpdateNodeRestraintCommand(
            model=model, node_id=node.id, new_restraint=FIXED
        )
        cmd.execute()
        cmd.undo()

        assert node.restraint.is_pinned


class TestMoveNodeByOffsetCommand:
    """Tests for MoveNodeByOffsetCommand."""

    def test_execute_moves_by_offset(self) -> None:
        """Execute should move node by offset."""
        model = StructuralModel()
        node = model.add_node(x=1, y=2, z=3)

        cmd = MoveNodeByOffsetCommand(
            model=model, node_id=node.id, dx=1, dy=1, dz=1
        )
        cmd.execute()

        assert node.position == (2, 3, 4)

    def test_undo_reverses_offset(self) -> None:
        """Undo should reverse the offset."""
        model = StructuralModel()
        node = model.add_node(x=5, y=5, z=5)

        cmd = MoveNodeByOffsetCommand(
            model=model, node_id=node.id, dx=2, dy=3, dz=4
        )
        cmd.execute()
        cmd.undo()

        assert node.position == (5, 5, 5)


class TestUndoRedoService:
    """Tests for UndoRedoService."""

    def test_execute_adds_to_history(self) -> None:
        """Execute should add command to undo history."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd = CreateNodeCommand(model=model, x=0, y=0, z=0)
        service.execute(cmd)

        assert service.can_undo
        assert not service.can_redo

    def test_undo(self) -> None:
        """Undo should reverse last command."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd = CreateNodeCommand(model=model, x=0, y=0, z=0)
        service.execute(cmd)
        assert model.node_count == 1

        service.undo()
        assert model.node_count == 0
        assert service.can_redo

    def test_redo(self) -> None:
        """Redo should re-execute undone command."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd = CreateNodeCommand(model=model, x=0, y=0, z=0)
        service.execute(cmd)
        service.undo()
        service.redo()

        assert model.node_count == 1

    def test_undo_redo_sequence(self) -> None:
        """Multiple undo/redo operations."""
        model = StructuralModel()
        service = UndoRedoService()

        # Create 3 nodes
        for i in range(3):
            cmd = CreateNodeCommand(model=model, x=i, y=0, z=0)
            service.execute(cmd)

        assert model.node_count == 3

        # Undo all
        service.undo()
        service.undo()
        service.undo()
        assert model.node_count == 0

        # Redo 2
        service.redo()
        service.redo()
        assert model.node_count == 2

    def test_new_command_clears_redo(self) -> None:
        """New command should clear redo stack."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd1 = CreateNodeCommand(model=model, x=0, y=0, z=0)
        service.execute(cmd1)
        service.undo()
        assert service.can_redo

        cmd2 = CreateNodeCommand(model=model, x=1, y=0, z=0)
        service.execute(cmd2)
        assert not service.can_redo

    def test_history_limit(self) -> None:
        """History should be limited."""
        model = StructuralModel()
        service = UndoRedoService(max_history=5)

        for i in range(10):
            cmd = CreateNodeCommand(model=model, x=i, y=0, z=0)
            service.execute(cmd)

        assert service.undo_count == 5

    def test_descriptions(self) -> None:
        """Descriptions should be available."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd = CreateNodeCommand(model=model, x=1, y=2, z=3)
        service.execute(cmd)

        assert service.undo_description is not None
        assert "1" in service.undo_description and "2" in service.undo_description

    def test_clear(self) -> None:
        """Clear should empty history."""
        model = StructuralModel()
        service = UndoRedoService()

        cmd = CreateNodeCommand(model=model, x=0, y=0, z=0)
        service.execute(cmd)
        service.clear()

        assert not service.can_undo
        assert not service.can_redo
