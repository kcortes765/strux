"""
Node model for structural analysis.

A node represents a point in 3D space where structural elements connect.
"""

from dataclasses import dataclass, field
from math import isfinite, sqrt
from typing import Any

from paz.core.constants import COORDINATE_PRECISION
from paz.core.exceptions import ValidationError
from paz.domain.model.restraint import FREE, Restraint


@dataclass
class Node:
    """
    Represents a structural node (joint) in 3D space.

    Attributes:
        id: Unique identifier for the node
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
        restraint: Boundary conditions at this node
    """

    id: int
    x: float
    y: float
    z: float
    restraint: Restraint = field(default_factory=lambda: FREE)

    def __post_init__(self) -> None:
        """Validate and round coordinates."""
        # Validate coordinates are finite numbers
        for coord, name in [(self.x, "x"), (self.y, "y"), (self.z, "z")]:
            if not isfinite(coord):
                raise ValidationError(
                    f"Coordinate {name} must be a finite number, got {coord}",
                    field=name,
                )

        # Round coordinates to specified precision
        self.x = round(self.x, COORDINATE_PRECISION)
        self.y = round(self.y, COORDINATE_PRECISION)
        self.z = round(self.z, COORDINATE_PRECISION)

    @property
    def position(self) -> tuple[float, float, float]:
        """Get position as tuple (x, y, z)."""
        return (self.x, self.y, self.z)

    @property
    def is_supported(self) -> bool:
        """Check if node has any restraints."""
        return not self.restraint.is_free

    def distance_to(self, other: "Node") -> float:
        """
        Calculate distance to another node.

        Args:
            other: The other node

        Returns:
            Euclidean distance between nodes
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return sqrt(dx * dx + dy * dy + dz * dz)

    def distance_to_point(self, x: float, y: float, z: float) -> float:
        """
        Calculate distance to a point.

        Args:
            x: X coordinate of point
            y: Y coordinate of point
            z: Z coordinate of point

        Returns:
            Euclidean distance to point
        """
        dx = self.x - x
        dy = self.y - y
        dz = self.z - z
        return sqrt(dx * dx + dy * dy + dz * dz)

    def move_to(self, x: float, y: float, z: float) -> None:
        """
        Move node to new position.

        Args:
            x: New X coordinate
            y: New Y coordinate
            z: New Z coordinate
        """
        self.x = round(x, COORDINATE_PRECISION)
        self.y = round(y, COORDINATE_PRECISION)
        self.z = round(z, COORDINATE_PRECISION)

    def move_by(self, dx: float, dy: float, dz: float) -> None:
        """
        Move node by offset.

        Args:
            dx: Offset in X direction
            dy: Offset in Y direction
            dz: Offset in Z direction
        """
        self.x = round(self.x + dx, COORDINATE_PRECISION)
        self.y = round(self.y + dy, COORDINATE_PRECISION)
        self.z = round(self.z + dz, COORDINATE_PRECISION)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "restraint": self.restraint.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        """Create from dictionary."""
        restraint_data = data.get("restraint", {})
        return cls(
            id=data["id"],
            x=float(data["x"]),
            y=float(data["y"]),
            z=float(data["z"]),
            restraint=Restraint.from_dict(restraint_data)
            if restraint_data
            else FREE,
        )

    def copy(self, new_id: int | None = None) -> "Node":
        """
        Create a copy of this node.

        Args:
            new_id: Optional new ID for the copy

        Returns:
            New Node instance with same properties
        """
        return Node(
            id=new_id if new_id is not None else self.id,
            x=self.x,
            y=self.y,
            z=self.z,
            restraint=self.restraint,
        )
