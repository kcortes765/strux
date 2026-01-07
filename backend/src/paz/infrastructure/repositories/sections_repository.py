"""
Sections repository for loading and managing section libraries.

Loads predefined sections from JSON files (AISC, Eurocode, etc.) and supports custom sections.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from paz.core.exceptions import SectionNotFoundError
from paz.core.logging_config import get_logger
from paz.domain.sections.section import (
    Section,
    SectionShape,
    SectionStandard,
)


if TYPE_CHECKING:
    from collections.abc import Iterator

logger = get_logger("sections_repository")


class SectionsRepository:
    """
    Repository for structural sections.

    Loads predefined sections from JSON files and manages custom sections.
    Supports searching and filtering by name, shape, and standard.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        """
        Initialize the sections repository.

        Args:
            data_path: Path to the data/sections directory.
                      Defaults to src/data/sections relative to this file.
        """
        if data_path is None:
            # Default to src/data/sections (4 levels up from this file to src/)
            data_path = (
                Path(__file__).parent.parent.parent.parent / "data" / "sections"
            )

        self._data_path = data_path
        self._sections: dict[str, Section] = {}
        self._loaded = False

    def _ensure_loaded(self) -> None:
        """Load sections if not already loaded."""
        if not self._loaded:
            self.load_all()

    def load_all(self) -> int:
        """
        Load all predefined sections from JSON files.

        Returns:
            Number of sections loaded
        """
        self._sections.clear()
        count = 0

        if not self._data_path.exists():
            logger.warning(f"Sections data path does not exist: {self._data_path}")
            self._loaded = True
            return 0

        for json_file in self._data_path.glob("*.json"):
            try:
                loaded = self._load_file(json_file)
                count += loaded
                logger.info(f"Loaded {loaded} sections from {json_file.name}")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.error(f"Failed to load sections from {json_file}: {e}")

        self._loaded = True
        logger.info(f"Total sections loaded: {count}")
        return count

    def _load_file(self, path: Path) -> int:
        """
        Load sections from a single JSON file.

        Args:
            path: Path to the JSON file

        Returns:
            Number of sections loaded
        """
        with path.open(encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for section_data in data.get("sections", []):
            try:
                section = Section.from_dict(section_data)
                # Use name as key for predefined sections
                self._sections[section.name] = section
                count += 1
            except Exception as e:
                logger.warning(
                    f"Failed to load section {section_data.get('name', '?')}: {e}"
                )

        return count

    def get(self, name: str) -> Section:
        """
        Get a section by name.

        Args:
            name: Section designation (e.g., "W14X30", "HSS8X4X1/2")

        Returns:
            The section

        Raises:
            SectionNotFoundError: If section not found
        """
        self._ensure_loaded()

        if name not in self._sections:
            raise SectionNotFoundError(name)

        return self._sections[name]

    def get_by_id(self, section_id: str) -> Section:
        """
        Get a section by UUID.

        Args:
            section_id: Section UUID as string

        Returns:
            The section

        Raises:
            SectionNotFoundError: If section not found
        """
        self._ensure_loaded()

        for section in self._sections.values():
            if str(section.id) == section_id:
                return section

        raise SectionNotFoundError(section_id)

    def exists(self, name: str) -> bool:
        """Check if a section exists by name."""
        self._ensure_loaded()
        return name in self._sections

    def all(self) -> list[Section]:
        """Get all sections."""
        self._ensure_loaded()
        return list(self._sections.values())

    def count(self) -> int:
        """Get total number of sections."""
        self._ensure_loaded()
        return len(self._sections)

    def iter(self) -> Iterator[Section]:
        """Iterate over all sections."""
        self._ensure_loaded()
        return iter(self._sections.values())

    def filter_by_shape(self, shape: SectionShape) -> list[Section]:
        """
        Get all sections of a specific shape.

        Args:
            shape: Shape to filter by (W, HSS_RECT, L, etc.)

        Returns:
            List of matching sections
        """
        self._ensure_loaded()
        return [s for s in self._sections.values() if s.shape == shape]

    def filter_by_standard(self, standard: SectionStandard) -> list[Section]:
        """
        Get all sections from a specific standard.

        Args:
            standard: Standard to filter by (AISC, Eurocode, etc.)

        Returns:
            List of matching sections
        """
        self._ensure_loaded()
        return [s for s in self._sections.values() if s.standard == standard]

    def search(self, query: str) -> list[Section]:
        """
        Search sections by name or description.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching sections
        """
        self._ensure_loaded()
        query_lower = query.lower()
        return [
            s
            for s in self._sections.values()
            if query_lower in s.name.lower() or query_lower in s.description.lower()
        ]

    def get_w_shapes(self) -> list[Section]:
        """Get all W (Wide Flange) sections."""
        return self.filter_by_shape(SectionShape.W)

    def get_hss_rect_shapes(self) -> list[Section]:
        """Get all HSS rectangular sections."""
        return self.filter_by_shape(SectionShape.HSS_RECT)

    def get_hss_round_shapes(self) -> list[Section]:
        """Get all HSS round sections."""
        return self.filter_by_shape(SectionShape.HSS_ROUND)

    def get_angles(self) -> list[Section]:
        """Get all angle (L) sections."""
        return self.filter_by_shape(SectionShape.L)

    def get_channels(self) -> list[Section]:
        """Get all channel (C) sections."""
        return self.filter_by_shape(SectionShape.C)

    def get_pipes(self) -> list[Section]:
        """Get all pipe sections."""
        return self.filter_by_shape(SectionShape.PIPE)

    def add_custom(self, section: Section) -> None:
        """
        Add a custom section to the repository.

        Args:
            section: The custom section to add
        """
        self._ensure_loaded()
        self._sections[section.name] = section
        logger.info(f"Added custom section: {section.name}")

    def remove_custom(self, name: str) -> bool:
        """
        Remove a custom section.

        Args:
            name: Name of the section to remove

        Returns:
            True if removed, False if not found or not custom
        """
        self._ensure_loaded()

        if name not in self._sections:
            return False

        section = self._sections[name]
        if not section.is_custom:
            logger.warning(f"Cannot remove predefined section: {name}")
            return False

        del self._sections[name]
        logger.info(f"Removed custom section: {name}")
        return True

    def get_names(self) -> list[str]:
        """Get list of all section names."""
        self._ensure_loaded()
        return list(self._sections.keys())

    def get_shapes(self) -> list[SectionShape]:
        """Get list of unique section shapes in the repository."""
        self._ensure_loaded()
        return list({s.shape for s in self._sections.values()})

    def get_standards(self) -> list[SectionStandard]:
        """Get list of unique standards in the repository."""
        self._ensure_loaded()
        return list({s.standard for s in self._sections.values()})
