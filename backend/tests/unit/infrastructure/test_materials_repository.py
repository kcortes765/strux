"""Tests for MaterialsRepository."""

from pathlib import Path

import pytest

from paz.core.exceptions import MaterialNotFoundError
from paz.domain.materials.material import Material, MaterialStandard, MaterialType
from paz.infrastructure.repositories.materials_repository import MaterialsRepository


class TestMaterialsRepository:
    """Tests for MaterialsRepository."""

    @pytest.fixture
    def repo(self) -> MaterialsRepository:
        """Create a repository with default data path."""
        return MaterialsRepository()

    def test_load_all_materials(self, repo: MaterialsRepository) -> None:
        """Should load materials from JSON files."""
        count = repo.load_all()
        assert count > 0
        assert repo.count() == count

    def test_get_material_by_name(self, repo: MaterialsRepository) -> None:
        """Should get a material by name."""
        material = repo.get("A36")
        assert material.name == "A36"
        assert material.material_type == MaterialType.STEEL

    def test_get_material_not_found(self, repo: MaterialsRepository) -> None:
        """Should raise error for unknown material."""
        with pytest.raises(MaterialNotFoundError):
            repo.get("NonExistent")

    def test_exists(self, repo: MaterialsRepository) -> None:
        """Should check if material exists."""
        assert repo.exists("A36") is True
        assert repo.exists("NonExistent") is False

    def test_all_materials(self, repo: MaterialsRepository) -> None:
        """Should return all materials."""
        materials = repo.all()
        assert len(materials) > 0
        assert all(isinstance(m, Material) for m in materials)

    def test_filter_by_type_steel(self, repo: MaterialsRepository) -> None:
        """Should filter materials by type."""
        steels = repo.filter_by_type(MaterialType.STEEL)
        assert len(steels) > 0
        assert all(m.material_type == MaterialType.STEEL for m in steels)

    def test_filter_by_type_concrete(self, repo: MaterialsRepository) -> None:
        """Should filter concrete materials."""
        concretes = repo.filter_by_type(MaterialType.CONCRETE)
        assert len(concretes) > 0
        assert all(m.material_type == MaterialType.CONCRETE for m in concretes)

    def test_filter_by_standard_astm(self, repo: MaterialsRepository) -> None:
        """Should filter materials by standard."""
        astm = repo.filter_by_standard(MaterialStandard.ASTM)
        assert len(astm) > 0
        assert all(m.standard == MaterialStandard.ASTM for m in astm)

    def test_filter_by_standard_nch(self, repo: MaterialsRepository) -> None:
        """Should filter NCh materials."""
        nch = repo.filter_by_standard(MaterialStandard.NCH)
        assert len(nch) > 0
        assert all(m.standard == MaterialStandard.NCH for m in nch)

    def test_filter_by_standard_eurocode(self, repo: MaterialsRepository) -> None:
        """Should filter Eurocode materials."""
        eurocode = repo.filter_by_standard(MaterialStandard.EUROCODE)
        assert len(eurocode) > 0
        assert all(m.standard == MaterialStandard.EUROCODE for m in eurocode)

    def test_search_by_name(self, repo: MaterialsRepository) -> None:
        """Should search materials by name."""
        results = repo.search("A36")
        assert len(results) >= 1
        assert any(m.name == "A36" for m in results)

    def test_search_by_description(self, repo: MaterialsRepository) -> None:
        """Should search materials by description."""
        results = repo.search("structural steel")
        assert len(results) >= 1

    def test_search_case_insensitive(self, repo: MaterialsRepository) -> None:
        """Search should be case insensitive."""
        results_lower = repo.search("a36")
        results_upper = repo.search("A36")
        assert len(results_lower) == len(results_upper)

    def test_get_steel_materials(self, repo: MaterialsRepository) -> None:
        """Convenience method for steel materials."""
        steels = repo.get_steel_materials()
        assert len(steels) > 0
        assert "A36" in [m.name for m in steels]

    def test_get_concrete_materials(self, repo: MaterialsRepository) -> None:
        """Convenience method for concrete materials."""
        concretes = repo.get_concrete_materials()
        assert len(concretes) > 0
        assert "H30" in [m.name for m in concretes]

    def test_add_custom_material(self, repo: MaterialsRepository) -> None:
        """Should add custom materials."""
        custom = Material(
            name="CustomSteel",
            material_type=MaterialType.STEEL,
            E=210_000_000,
            nu=0.3,
            rho=7850,
            fy=300_000,
            fu=450_000,
            is_custom=True,
        )
        repo.add_custom(custom)
        assert repo.exists("CustomSteel")
        retrieved = repo.get("CustomSteel")
        assert retrieved.E == 210_000_000

    def test_remove_custom_material(self, repo: MaterialsRepository) -> None:
        """Should remove custom materials."""
        custom = Material(
            name="ToRemove",
            material_type=MaterialType.STEEL,
            E=200_000_000,
            nu=0.3,
            rho=7850,
            is_custom=True,
        )
        repo.add_custom(custom)
        assert repo.exists("ToRemove")

        result = repo.remove_custom("ToRemove")
        assert result is True
        assert not repo.exists("ToRemove")

    def test_remove_predefined_material_fails(self, repo: MaterialsRepository) -> None:
        """Should not remove predefined materials."""
        result = repo.remove_custom("A36")
        assert result is False
        assert repo.exists("A36")

    def test_remove_nonexistent_material(self, repo: MaterialsRepository) -> None:
        """Should return False for nonexistent materials."""
        result = repo.remove_custom("NonExistent")
        assert result is False

    def test_get_names(self, repo: MaterialsRepository) -> None:
        """Should return list of material names."""
        names = repo.get_names()
        assert len(names) > 0
        assert "A36" in names
        assert "H30" in names

    def test_get_types(self, repo: MaterialsRepository) -> None:
        """Should return unique material types."""
        types = repo.get_types()
        assert MaterialType.STEEL in types
        assert MaterialType.CONCRETE in types

    def test_get_standards(self, repo: MaterialsRepository) -> None:
        """Should return unique standards."""
        standards = repo.get_standards()
        assert MaterialStandard.ASTM in standards
        assert MaterialStandard.NCH in standards
        assert MaterialStandard.EUROCODE in standards

    def test_iter_materials(self, repo: MaterialsRepository) -> None:
        """Should iterate over materials."""
        materials_list = list(repo.iter())
        assert len(materials_list) > 0
        assert len(materials_list) == repo.count()

    def test_empty_data_path(self, tmp_path: Path) -> None:
        """Should handle empty data path gracefully."""
        empty_path = tmp_path / "empty"
        empty_path.mkdir()
        repo = MaterialsRepository(data_path=empty_path)
        count = repo.load_all()
        assert count == 0
        assert repo.count() == 0

    def test_nonexistent_data_path(self, tmp_path: Path) -> None:
        """Should handle nonexistent data path gracefully."""
        repo = MaterialsRepository(data_path=tmp_path / "nonexistent")
        count = repo.load_all()
        assert count == 0
