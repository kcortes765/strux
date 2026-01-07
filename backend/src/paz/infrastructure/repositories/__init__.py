"""
Repositories - Data access patterns for materials, sections, and projects.
"""

from paz.infrastructure.repositories.materials_repository import MaterialsRepository
from paz.infrastructure.repositories.sections_repository import SectionsRepository


__all__ = [
    "MaterialsRepository",
    "SectionsRepository",
]
