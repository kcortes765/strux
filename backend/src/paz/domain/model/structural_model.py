"""
Structural model containing all elements of a structure.

The StructuralModel is the central container for nodes, frames, materials,
sections, and other structural components.
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from paz.core.constants import MAX_NODES, NODE_DUPLICATE_TOLERANCE
from paz.core.exceptions import DuplicateNodeError, NodeError, ValidationError
from paz.domain.model.node import Node
from paz.domain.model.restraint import Restraint


@dataclass
class StructuralModel:
    """
    Container for all structural model data.

    Manages nodes, frames, and provides validation and queries.
    """

    _nodes: dict[int, Node] = field(default_factory=dict)
    _next_node_id: int = 1

    # Node operations

    @property
    def nodes(self) -> list[Node]:
        """Get all nodes as a list."""
        return list(self._nodes.values())

    @property
    def node_count(self) -> int:
        """Get the number of nodes."""
        return len(self._nodes)

    def get_node(self, node_id: int) -> Node:
        """
        Get a node by ID.

        Args:
            node_id: The node ID

        Returns:
            The node

        Raises:
            NodeError: If node doesn't exist
        """
        if node_id not in self._nodes:
            raise NodeError(f"Node {node_id} not found", node_id=node_id)
        return self._nodes[node_id]

    def has_node(self, node_id: int) -> bool:
        """Check if a node exists."""
        return node_id in self._nodes

    def add_node(
        self,
        x: float,
        y: float,
        z: float,
        restraint: Restraint | None = None,
        node_id: int | None = None,
        check_duplicate: bool = True,
    ) -> Node:
        """
        Add a new node to the model.

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            restraint: Optional boundary conditions
            node_id: Optional specific ID (auto-generated if None)
            check_duplicate: Whether to check for duplicate nodes

        Returns:
            The created node

        Raises:
            ValidationError: If max nodes exceeded
            DuplicateNodeError: If a node exists at the same location
        """
        # Check limit
        if self.node_count >= MAX_NODES:
            raise ValidationError(
                f"Maximum number of nodes ({MAX_NODES}) exceeded",
                field="nodes",
            )

        # Check for duplicate
        if check_duplicate:
            existing = self.find_node_at(x, y, z)
            if existing is not None:
                raise DuplicateNodeError(x, y, z, existing.id)

        # Determine ID
        if node_id is None:
            node_id = self._next_node_id
            self._next_node_id += 1
        else:
            if node_id in self._nodes:
                raise NodeError(f"Node ID {node_id} already exists", node_id=node_id)
            if node_id >= self._next_node_id:
                self._next_node_id = node_id + 1

        # Create and add node
        from paz.domain.model.restraint import FREE

        node = Node(
            id=node_id,
            x=x,
            y=y,
            z=z,
            restraint=restraint if restraint is not None else FREE,
        )
        self._nodes[node_id] = node

        return node

    def remove_node(self, node_id: int) -> Node:
        """
        Remove a node from the model.

        Args:
            node_id: ID of node to remove

        Returns:
            The removed node

        Raises:
            NodeError: If node doesn't exist
        """
        if node_id not in self._nodes:
            raise NodeError(f"Node {node_id} not found", node_id=node_id)

        # TODO: Check if node is used by any frames
        return self._nodes.pop(node_id)

    def update_node(
        self,
        node_id: int,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        restraint: Restraint | None = None,
    ) -> Node:
        """
        Update node properties.

        Args:
            node_id: ID of node to update
            x: New X coordinate (None to keep current)
            y: New Y coordinate (None to keep current)
            z: New Z coordinate (None to keep current)
            restraint: New restraint (None to keep current)

        Returns:
            The updated node

        Raises:
            NodeError: If node doesn't exist
        """
        node = self.get_node(node_id)

        if x is not None:
            node.x = x
        if y is not None:
            node.y = y
        if z is not None:
            node.z = z
        if restraint is not None:
            node.restraint = restraint

        return node

    def find_node_at(
        self,
        x: float,
        y: float,
        z: float,
        tolerance: float = NODE_DUPLICATE_TOLERANCE,
    ) -> Node | None:
        """
        Find a node at the given coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate
            tolerance: Distance tolerance for matching

        Returns:
            Node at location, or None if not found
        """
        for node in self._nodes.values():
            if node.distance_to_point(x, y, z) <= tolerance:
                return node
        return None

    def find_nodes_in_box(
        self,
        x_min: float,
        y_min: float,
        z_min: float,
        x_max: float,
        y_max: float,
        z_max: float,
    ) -> list[Node]:
        """
        Find all nodes within a bounding box.

        Args:
            x_min, y_min, z_min: Minimum coordinates
            x_max, y_max, z_max: Maximum coordinates

        Returns:
            List of nodes within the box
        """
        return [
            node
            for node in self._nodes.values()
            if x_min <= node.x <= x_max
            and y_min <= node.y <= y_max
            and z_min <= node.z <= z_max
        ]

    def get_supported_nodes(self) -> list[Node]:
        """Get all nodes with restraints."""
        return [node for node in self._nodes.values() if node.is_supported]

    def iter_nodes(self) -> Iterator[Node]:
        """Iterate over all nodes."""
        return iter(self._nodes.values())

    # Serialization

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "nodes": [node.to_dict() for node in self._nodes.values()],
            "next_node_id": self._next_node_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StructuralModel":
        """Create from dictionary."""
        model = cls()

        for node_data in data.get("nodes", []):
            node = Node.from_dict(node_data)
            model._nodes[node.id] = node

        model._next_node_id = data.get("next_node_id", 1)
        if model._nodes:
            max_id = max(model._nodes.keys())
            if model._next_node_id <= max_id:
                model._next_node_id = max_id + 1

        return model

    def clear(self) -> None:
        """Remove all nodes and reset."""
        self._nodes.clear()
        self._next_node_id = 1
