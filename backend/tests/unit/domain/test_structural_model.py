"""Tests for StructuralModel."""

import pytest

from paz.core.exceptions import DuplicateNodeError, NodeError, ValidationError
from paz.domain.model.node import Node
from paz.domain.model.restraint import FIXED, PINNED
from paz.domain.model.structural_model import StructuralModel


class TestStructuralModelNodes:
    """Tests for node operations in StructuralModel."""

    def test_empty_model(self) -> None:
        """New model should have no nodes."""
        model = StructuralModel()
        assert model.node_count == 0
        assert model.nodes == []

    def test_add_node(self) -> None:
        """Add a node to the model."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)
        assert model.node_count == 1
        assert node.id == 1
        assert node.position == (0, 0, 0)

    def test_add_multiple_nodes(self) -> None:
        """Add multiple nodes with auto-incrementing IDs."""
        model = StructuralModel()
        n1 = model.add_node(x=0, y=0, z=0)
        n2 = model.add_node(x=1, y=0, z=0)
        n3 = model.add_node(x=2, y=0, z=0)

        assert n1.id == 1
        assert n2.id == 2
        assert n3.id == 3
        assert model.node_count == 3

    def test_add_node_with_specific_id(self) -> None:
        """Add a node with a specific ID."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0, node_id=100)
        assert node.id == 100

    def test_add_node_with_restraint(self) -> None:
        """Add a node with restraint."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0, restraint=FIXED)
        assert node.restraint.is_fixed

    def test_add_duplicate_node_raises(self) -> None:
        """Adding a node at existing location should raise."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)

        with pytest.raises(DuplicateNodeError):
            model.add_node(x=0, y=0, z=0)

    def test_add_duplicate_with_tolerance(self) -> None:
        """Nodes within tolerance should be detected as duplicates."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)

        with pytest.raises(DuplicateNodeError):
            model.add_node(x=0.0001, y=0, z=0)  # Within default tolerance

    def test_add_duplicate_check_disabled(self) -> None:
        """Can add duplicate when check is disabled."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)
        model.add_node(x=0, y=0, z=0, check_duplicate=False)
        assert model.node_count == 2

    def test_get_node(self) -> None:
        """Get a node by ID."""
        model = StructuralModel()
        created = model.add_node(x=1, y=2, z=3)
        retrieved = model.get_node(created.id)
        assert retrieved is created

    def test_get_nonexistent_node_raises(self) -> None:
        """Getting nonexistent node should raise."""
        model = StructuralModel()
        with pytest.raises(NodeError):
            model.get_node(999)

    def test_has_node(self) -> None:
        """has_node should return correct result."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)
        assert model.has_node(node.id)
        assert not model.has_node(999)

    def test_remove_node(self) -> None:
        """Remove a node from the model."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)
        removed = model.remove_node(node.id)
        assert removed.id == node.id
        assert model.node_count == 0

    def test_remove_nonexistent_node_raises(self) -> None:
        """Removing nonexistent node should raise."""
        model = StructuralModel()
        with pytest.raises(NodeError):
            model.remove_node(999)

    def test_update_node_position(self) -> None:
        """Update node coordinates."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)
        updated = model.update_node(node.id, x=5, y=6, z=7)
        assert updated.position == (5, 6, 7)

    def test_update_node_partial(self) -> None:
        """Update only some coordinates."""
        model = StructuralModel()
        node = model.add_node(x=1, y=2, z=3)
        model.update_node(node.id, x=10)
        assert node.position == (10, 2, 3)

    def test_update_node_restraint(self) -> None:
        """Update node restraint."""
        model = StructuralModel()
        node = model.add_node(x=0, y=0, z=0)
        model.update_node(node.id, restraint=PINNED)
        assert node.restraint.is_pinned

    def test_find_node_at(self) -> None:
        """Find a node at specific coordinates."""
        model = StructuralModel()
        node = model.add_node(x=5, y=6, z=7)
        found = model.find_node_at(5, 6, 7)
        assert found is node

    def test_find_node_at_not_found(self) -> None:
        """find_node_at returns None if not found."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)
        found = model.find_node_at(100, 100, 100)
        assert found is None

    def test_find_nodes_in_box(self) -> None:
        """Find nodes within a bounding box."""
        model = StructuralModel()
        n1 = model.add_node(x=0, y=0, z=0)
        n2 = model.add_node(x=5, y=5, z=5)
        n3 = model.add_node(x=10, y=10, z=10)

        found = model.find_nodes_in_box(0, 0, 0, 6, 6, 6)
        assert len(found) == 2
        assert n1 in found
        assert n2 in found
        assert n3 not in found

    def test_get_supported_nodes(self) -> None:
        """Get nodes with restraints."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0, restraint=FIXED)
        model.add_node(x=1, y=0, z=0)  # Free
        model.add_node(x=2, y=0, z=0, restraint=PINNED)

        supported = model.get_supported_nodes()
        assert len(supported) == 2

    def test_iter_nodes(self) -> None:
        """Iterate over nodes."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)
        model.add_node(x=1, y=0, z=0)
        model.add_node(x=2, y=0, z=0)

        count = sum(1 for _ in model.iter_nodes())
        assert count == 3

    def test_clear(self) -> None:
        """Clear all nodes."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)
        model.add_node(x=1, y=0, z=0)
        model.clear()
        assert model.node_count == 0

    def test_to_dict_from_dict_roundtrip(self) -> None:
        """Serialization roundtrip should preserve data."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0, restraint=FIXED)
        model.add_node(x=5, y=0, z=0)
        model.add_node(x=5, y=3, z=0, restraint=PINNED)

        data = model.to_dict()
        restored = StructuralModel.from_dict(data)

        assert restored.node_count == 3
        assert restored.get_node(1).restraint.is_fixed
        assert restored.get_node(3).restraint.is_pinned

    def test_node_id_continuity_after_restore(self) -> None:
        """Next node ID should be correct after restore."""
        model = StructuralModel()
        model.add_node(x=0, y=0, z=0)
        model.add_node(x=1, y=0, z=0)

        data = model.to_dict()
        restored = StructuralModel.from_dict(data)

        new_node = restored.add_node(x=2, y=0, z=0)
        assert new_node.id == 3
