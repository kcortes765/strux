"""
Materials repository for loading and managing material libraries.

Loads predefined materials from JSON files and supports custom materials.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from paz.core.exceptions import MaterialNotFoundError
from paz.core.logging_config import get_logger
from paz.domain.materials.material import (
    Material,
    MaterialStandard,
    MaterialType,
)


if TYPE_CHECKING:
    from collections.abc import Iterator

logger = get_logger("materials_repository")


class MaterialsRepository:
    """
    Repository for structural materials.

    Loads predefined materials from JSON files and manages custom materials.
    Supports searching and filtering by name, type, and standard.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        """
        Initialize the materials repository.

        Args:
            data_path: Path to the data/materials directory.
                      Defaults to src/data/materials relative to this file.
        """
        if data_path is None:
            # Default to src/data/materials (4 levels up from this file to src/)
            data_path = (
                Path(__file__).parent.parent.parent.parent / "data" / "materials"
            )

        self._data_path = data_path
        self._materials: dict[str, Material] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Load materials if not already loaded."""
        if not self._loaded:
            self.load_all()

    def load_all(self) -> int:
        """
        Load all predefined materials from JSON files.

        Returns:
            Number of materials loaded
        """
        self._materials.clear()
        count = 0

        if not self._data_path.exists():
            logger.warning(f"Materials data path does not exist: {self._data_path}")
            self._loaded = True
            return 0

        for json_file in self._data_path.glob("*.json"):
            try:
                loaded = self._load_file(json_file)
                count += loaded
                logger.info(f"Loaded {loaded} materials from {json_file.name}")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Failed to load materials from {json_file}: {e}")

        self._loaded = True
        logger.info(f"Total materials loaded: {count}")
        return count

    def _load_file(self, path: Path) -> int:
        """
        Load materials from a single JSON file.

        Args:
            path: Path to the JSON file

        Returns:
            Number of materials loaded
        """
        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for mat_data in data.get("materials", []):
            try:
                material = Material.from_dict(mat_data)
                # Use name as key for predefined materials
                self._materials[material.name] = material
                count += 1
            except Exception as e:
                logger.warning(f"Failed to load material {mat_data.get('name', '?')}: {e}")

        return count

    def get(self, name: str) -> Material:
        """
        Get a material by name.

        Args:
            name: Material name (e.g., "A36", "H30")

        Returns:
            The material

        Raises:
            MaterialNotFoundError: If material not found
        """
        self._ensure_loaded()

        if name not in self._materials:
            raise MaterialNotFoundError(name)

        return self._materials[name]

    def get_by_id(self, material_id: str) -> Material:
        """
        Get a material by UUID.

        Args:
            material_id: Material UUID as string

        Returns:
            The material

        Raises:
            MaterialNotFoundError: If material not found
        """
        self._ensure_loaded()

        for material in self._materials.values():
            if str(material.id) == material_id:
                return material

        raise MaterialNotFoundError(material_id)

    def exists(self, name: str) -> bool:
        """Check if a material exists by name."""
        self._ensure_loaded()
        return name in self._materials

    def all(self) -> list[Material]:
        """Get all materials."""
        self._ensure_loaded()
        return list(self._materials.values())

    def count(self) -> int:
        """Get total number of materials."""
        self._ensure_loaded()
        return len(self._materials)

    def iter(self) -> Iterator[Material]:
        """Iterate over all materials."""
        self._ensure_loaded()
        return iter(self._materials.values())

    def filter_by_type(self, material_type: MaterialType) -> list[Material]:
        """
        Get all materials of a specific type.

        Args:
            material_type: Type to filter by (steel, concrete, etc.)

        Returns:
            List of matching materials
        """
        self._ensure_loaded()
        return [m for m in self._materials.values() if m.material_type == material_type]

    def filter_by_standard(self, standard: MaterialStandard) -> list[Material]:
        """
        Get all materials from a specific standard.

        Args:
            standard: Standard to filter by (ASTM, NCh, Eurocode, etc.)

        Returns:
            List of matching materials
        """
        self._ensure_loaded()
        return [m for m in self._materials.values() if m.standard == standard]

    def search(self, query: str) -> list[Material]:
        """
        Search materials by name or description.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching materials
        """
        self._ensure_loaded()
        query_lower = query.lower()
        return [
            m
            for m in self._materials.values()
            if query_lower in m.name.lower() or query_lower in m.description.lower()
        ]

    def get_steel_materials(self) -> list[Material]:
        """Get all steel materials."""
        return self.filter_by_type(MaterialType.STEEL)

    def get_concrete_materials(self) -> list[Material]:
        """Get all concrete materials."""
        return self.filter_by_type(MaterialType.CONCRETE)

    def add_custom(self, material: Material) -> None:
        """
        Add a custom material to the repository.

        Args:
            material: The custom material to add
        """
        self._ensure_loaded()
        self._materials[material.name] = material
        logger.info(f"Added custom material: {material.name}")

    def remove_custom(self, name: str) -> bool:
        """
        Remove a custom material.

        Args:
            name: Name of the material to remove

        Returns:
            True if removed, False if not found or not custom
        """
        self._ensure_loaded()

        if name not in self._materials:
            return False

        material = self._materials[name]
        if not material.is_custom:
            logger.warning(f"Cannot remove predefined material: {name}")
            return False

        del self._materials[name]
        logger.info(f"Removed custom material: {name}")
        return True

    def get_names(self) -> list[str]:
        """Get list of all material names."""
        self._ensure_loaded()
        return list(self._materials.keys())

    def get_types(self) -> list[MaterialType]:
        """Get list of unique material types in the repository."""
        self._ensure_loaded()
        return list({m.material_type for m in self._materials.values()})

    def get_standards(self) -> list[MaterialStandard]:
        """Get list of unique standards in the repository."""
        self._ensure_loaded()
        return list({m.standard for m in self._materials.values()})
