"""Tests for Node and Restraint models."""

import pytest
from math import sqrt

from paz.domain.model.node import Node
from paz.domain.model.restraint import (
    Restraint,
    FREE,
    FIXED,
    PINNED,
    ROLLER_X,
)


class TestRestraint:
    """Tests for Restraint dataclass."""

    def test_default_is_free(self) -> None:
        """Default restraint should be all free."""
        r = Restraint()
        assert r.is_free
        assert not r.is_fixed

    def test_fixed_preset(self) -> None:
        """FIXED preset should have all DOFs restrained."""
        assert FIXED.is_fixed
        assert not FIXED.is_free

    def test_pinned_preset(self) -> None:
        """PINNED preset should have translations fixed, rotations free."""
        assert PINNED.is_pinned
        assert PINNED.ux and PINNED.uy and PINNED.uz
        assert not PINNED.rx and not PINNED.ry and not PINNED.rz

    def test_roller_x(self) -> None:
        """ROLLER_X should allow movement in X only."""
        assert not ROLLER_X.ux  # Free in X
        assert ROLLER_X.uy and ROLLER_X.uz  # Fixed in Y, Z

    def test_to_list(self) -> None:
        """to_list should return correct order."""
        r = Restraint(ux=True, uy=False, uz=True, rx=False, ry=True, rz=False)
        assert r.to_list() == [True, False, True, False, True, False]

    def test_to_int_list(self) -> None:
        """to_int_list should return 1s and 0s."""
        assert FIXED.to_int_list() == [1, 1, 1, 1, 1, 1]
        assert FREE.to_int_list() == [0, 0, 0, 0, 0, 0]

    def test_from_list(self) -> None:
        """from_list should create correct restraint."""
        r = Restraint.from_list([1, 0, 1, 0, 1, 0])
        assert r.ux and not r.uy and r.uz
        assert not r.rx and r.ry and not r.rz

    def test_from_list_wrong_length_raises(self) -> None:
        """from_list should raise for wrong length."""
        with pytest.raises(ValueError):
            Restraint.from_list([1, 0, 1])

    def test_to_dict_from_dict_roundtrip(self) -> None:
        """Serialization roundtrip should preserve data."""
        original = Restraint(ux=True, uz=True, ry=True)
        restored = Restraint.from_dict(original.to_dict())
        assert restored == original


class TestNode:
    """Tests for Node dataclass."""

    def test_create_simple_node(self) -> None:
        """Create a node with coordinates."""
        node = Node(id=1, x=1.0, y=2.0, z=3.0)
        assert node.id == 1
        assert node.x == 1.0
        assert node.y == 2.0
        assert node.z == 3.0
        assert node.restraint.is_free

    def test_create_node_with_restraint(self) -> None:
        """Create a node with restraint."""
        node = Node(id=1, x=0, y=0, z=0, restraint=FIXED)
        assert node.is_supported
        assert node.restraint.is_fixed

    def test_position_property(self) -> None:
        """position should return tuple."""
        node = Node(id=1, x=1.5, y=2.5, z=3.5)
        assert node.position == (1.5, 2.5, 3.5)

    def test_distance_to_same_point(self) -> None:
        """Distance to same point should be zero."""
        n1 = Node(id=1, x=0, y=0, z=0)
        n2 = Node(id=2, x=0, y=0, z=0)
        assert n1.distance_to(n2) == 0.0

    def test_distance_to_other_node(self) -> None:
        """Distance calculation should be correct."""
        n1 = Node(id=1, x=0, y=0, z=0)
        n2 = Node(id=2, x=3, y=4, z=0)
        assert n1.distance_to(n2) == 5.0  # 3-4-5 triangle

    def test_distance_to_3d(self) -> None:
        """3D distance calculation."""
        n1 = Node(id=1, x=0, y=0, z=0)
        n2 = Node(id=2, x=1, y=1, z=1)
        assert abs(n1.distance_to(n2) - sqrt(3)) < 1e-9

    def test_distance_to_point(self) -> None:
        """Distance to a point in space."""
        node = Node(id=1, x=0, y=0, z=0)
        assert node.distance_to_point(1, 0, 0) == 1.0

    def test_move_to(self) -> None:
        """move_to should update coordinates."""
        node = Node(id=1, x=0, y=0, z=0)
        node.move_to(5.0, 6.0, 7.0)
        assert node.position == (5.0, 6.0, 7.0)

    def test_move_by(self) -> None:
        """move_by should add offset."""
        node = Node(id=1, x=1, y=2, z=3)
        node.move_by(1, 1, 1)
        assert node.position == (2.0, 3.0, 4.0)

    def test_coordinates_rounded_to_precision(self) -> None:
        """Coordinates should be rounded."""
        node = Node(id=1, x=1.123456789, y=2.987654321, z=3.111111111)
        assert node.x == 1.123457  # 6 decimal places
        assert node.y == 2.987654

    def test_to_dict_from_dict_roundtrip(self) -> None:
        """Serialization roundtrip should preserve data."""
        original = Node(id=42, x=1.5, y=2.5, z=3.5, restraint=PINNED)
        restored = Node.from_dict(original.to_dict())
        assert restored.id == original.id
        assert restored.position == original.position
        assert restored.restraint == original.restraint

    def test_copy_with_new_id(self) -> None:
        """copy should create new node with different ID."""
        original = Node(id=1, x=1, y=2, z=3, restraint=FIXED)
        copied = original.copy(new_id=2)
        assert copied.id == 2
        assert copied.position == original.position
        assert copied.restraint == original.restraint

    def test_copy_without_new_id(self) -> None:
        """copy without new_id should keep same ID."""
        original = Node(id=1, x=1, y=2, z=3)
        copied = original.copy()
        assert copied.id == original.id

    def test_infinite_x_raises_error(self) -> None:
        """Creating node with infinite x should raise ValidationError."""
        from paz.core.exceptions import ValidationError

        with pytest.raises(ValidationError, match="x must be a finite number"):
            Node(id=1, x=float("inf"), y=0, z=0)

    def test_infinite_y_raises_error(self) -> None:
        """Creating node with infinite y should raise ValidationError."""
        from paz.core.exceptions import ValidationError

        with pytest.raises(ValidationError, match="y must be a finite number"):
            Node(id=1, x=0, y=float("-inf"), z=0)

    def test_nan_z_raises_error(self) -> None:
        """Creating node with NaN z should raise ValidationError."""
        from paz.core.exceptions import ValidationError

        with pytest.raises(ValidationError, match="z must be a finite number"):
            Node(id=1, x=0, y=0, z=float("nan"))
