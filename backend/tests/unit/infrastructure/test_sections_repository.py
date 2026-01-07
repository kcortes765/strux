"""Tests for SectionsRepository."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from paz.core.exceptions import SectionNotFoundError
from paz.domain.sections.section import Section, SectionShape, SectionStandard
from paz.infrastructure.repositories.sections_repository import SectionsRepository


class TestSectionsRepository:
    """Tests for SectionsRepository."""

    @pytest.fixture
    def temp_data_dir(self) -> Path:
        """Create a temporary data directory with test sections."""
        with TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir)

            # Create test W shapes
            w_shapes = {
                "sections": [
                    {
                        "name": "W14X30",
                        "shape": "W",
                        "standard": "AISC",
                        "A": 0.00567,
                        "Ix": 1.21e-4,
                        "Iy": 8.14e-6,
                        "Sx": 6.89e-4,
                        "Sy": 9.54e-5,
                        "d": 0.351,
                        "bf": 0.171,
                        "tw": 0.00686,
                        "tf": 0.00978,
                        "W": 44.6,
                        "description": "AISC W14X30",
                        "is_custom": False,
                    },
                    {
                        "name": "W12X26",
                        "shape": "W",
                        "standard": "AISC",
                        "A": 0.00494,
                        "Ix": 8.47e-5,
                        "Iy": 7.19e-6,
                        "d": 0.310,
                        "bf": 0.165,
                        "description": "AISC W12X26",
                        "is_custom": False,
                    },
                ]
            }

            # Create test HSS shapes
            hss_shapes = {
                "sections": [
                    {
                        "name": "HSS8X4X1/2",
                        "shape": "HSS_RECT",
                        "standard": "AISC",
                        "A": 0.00361,
                        "Ix": 4.52e-5,
                        "Iy": 1.53e-5,
                        "t": 0.0127,
                        "description": "AISC HSS rectangular",
                        "is_custom": False,
                    },
                ]
            }

            with (data_path / "aisc_w.json").open("w") as f:
                json.dump(w_shapes, f)

            with (data_path / "aisc_hss.json").open("w") as f:
                json.dump(hss_shapes, f)

            yield data_path

    @pytest.fixture
    def repository(self, temp_data_dir: Path) -> SectionsRepository:
        """Create a repository with test data."""
        return SectionsRepository(data_path=temp_data_dir)

    def test_load_all_sections(self, repository: SectionsRepository) -> None:
        """Test loading all sections from JSON files."""
        count = repository.load_all()
        assert count == 3  # 2 W shapes + 1 HSS

    def test_get_section_by_name(self, repository: SectionsRepository) -> None:
        """Test getting a section by name."""
        section = repository.get("W14X30")
        assert section.name == "W14X30"
        assert section.shape == SectionShape.W
        assert section.standard == SectionStandard.AISC
        assert section.A == 0.00567
        assert section.d == 0.351

    def test_get_section_not_found(self, repository: SectionsRepository) -> None:
        """Test that missing section raises SectionNotFoundError."""
        with pytest.raises(SectionNotFoundError, match="W99X999"):
            repository.get("W99X999")

    def test_exists(self, repository: SectionsRepository) -> None:
        """Test checking if section exists."""
        assert repository.exists("W14X30") is True
        assert repository.exists("W12X26") is True
        assert repository.exists("NonExistent") is False

    def test_all_sections(self, repository: SectionsRepository) -> None:
        """Test getting all sections."""
        sections = repository.all()
        assert len(sections) == 3
        names = [s.name for s in sections]
        assert "W14X30" in names
        assert "W12X26" in names
        assert "HSS8X4X1/2" in names

    def test_filter_by_shape(self, repository: SectionsRepository) -> None:
        """Test filtering sections by shape."""
        w_shapes = repository.filter_by_shape(SectionShape.W)
        assert len(w_shapes) == 2

        hss_shapes = repository.filter_by_shape(SectionShape.HSS_RECT)
        assert len(hss_shapes) == 1
        assert hss_shapes[0].name == "HSS8X4X1/2"

        l_shapes = repository.filter_by_shape(SectionShape.L)
        assert len(l_shapes) == 0

    def test_filter_by_standard(self, repository: SectionsRepository) -> None:
        """Test filtering sections by standard."""
        aisc = repository.filter_by_standard(SectionStandard.AISC)
        assert len(aisc) == 3

        custom = repository.filter_by_standard(SectionStandard.CUSTOM)
        assert len(custom) == 0

    def test_search_by_name(self, repository: SectionsRepository) -> None:
        """Test searching sections by name."""
        results = repository.search("W14")
        assert len(results) == 1
        assert results[0].name == "W14X30"

    def test_search_by_description(self, repository: SectionsRepository) -> None:
        """Test searching sections by description."""
        results = repository.search("rectangular")
        assert len(results) == 1
        assert results[0].name == "HSS8X4X1/2"

    def test_search_case_insensitive(self, repository: SectionsRepository) -> None:
        """Test that search is case-insensitive."""
        results = repository.search("w14")
        assert len(results) == 1

        results = repository.search("AISC")
        assert len(results) == 3

    def test_get_w_shapes(self, repository: SectionsRepository) -> None:
        """Test getting all W shapes."""
        w_shapes = repository.get_w_shapes()
        assert len(w_shapes) == 2
        assert all(s.shape == SectionShape.W for s in w_shapes)

    def test_get_hss_rect_shapes(self, repository: SectionsRepository) -> None:
        """Test getting all HSS rectangular shapes."""
        hss = repository.get_hss_rect_shapes()
        assert len(hss) == 1
        assert hss[0].shape == SectionShape.HSS_RECT

    def test_add_custom_section(self, repository: SectionsRepository) -> None:
        """Test adding a custom section."""
        custom = Section(
            name="Custom-I",
            shape=SectionShape.CUSTOM,
            A=0.01,
            Ix=1e-4,
            Iy=1e-5,
            is_custom=True,
        )
        repository.add_custom(custom)

        assert repository.exists("Custom-I")
        retrieved = repository.get("Custom-I")
        assert retrieved.A == 0.01

    def test_remove_custom_section(self, repository: SectionsRepository) -> None:
        """Test removing a custom section."""
        custom = Section(
            name="ToRemove",
            shape=SectionShape.CUSTOM,
            A=0.01,
            Ix=1e-4,
            Iy=1e-5,
            is_custom=True,
        )
        repository.add_custom(custom)
        assert repository.exists("ToRemove")

        result = repository.remove_custom("ToRemove")
        assert result is True
        assert not repository.exists("ToRemove")

    def test_remove_predefined_section_fails(self, repository: SectionsRepository) -> None:
        """Test that removing a predefined section fails."""
        result = repository.remove_custom("W14X30")
        assert result is False
        assert repository.exists("W14X30")

    def test_remove_nonexistent_section(self, repository: SectionsRepository) -> None:
        """Test removing a nonexistent section returns False."""
        result = repository.remove_custom("NonExistent")
        assert result is False

    def test_get_names(self, repository: SectionsRepository) -> None:
        """Test getting list of section names."""
        names = repository.get_names()
        assert len(names) == 3
        assert "W14X30" in names
        assert "W12X26" in names
        assert "HSS8X4X1/2" in names

    def test_get_shapes(self, repository: SectionsRepository) -> None:
        """Test getting unique shapes in repository."""
        shapes = repository.get_shapes()
        assert SectionShape.W in shapes
        assert SectionShape.HSS_RECT in shapes
        assert len(shapes) == 2

    def test_get_standards(self, repository: SectionsRepository) -> None:
        """Test getting unique standards in repository."""
        standards = repository.get_standards()
        assert SectionStandard.AISC in standards
        assert len(standards) == 1

    def test_iter_sections(self, repository: SectionsRepository) -> None:
        """Test iterating over sections."""
        sections = list(repository.iter())
        assert len(sections) == 3

    def test_count(self, repository: SectionsRepository) -> None:
        """Test counting sections."""
        assert repository.count() == 3

    def test_empty_data_path(self) -> None:
        """Test repository with empty data directory."""
        with TemporaryDirectory() as tmpdir:
            repo = SectionsRepository(data_path=Path(tmpdir))
            count = repo.load_all()
            assert count == 0
            assert repo.all() == []

    def test_nonexistent_data_path(self) -> None:
        """Test repository with nonexistent data path."""
        repo = SectionsRepository(data_path=Path("/nonexistent/path"))
        count = repo.load_all()
        assert count == 0


class TestSectionsRepositoryWithRealData:
    """Tests using real AISC data."""

    @pytest.fixture
    def repository(self) -> SectionsRepository:
        """Create repository with real data."""
        return SectionsRepository()

    def test_load_real_data(self, repository: SectionsRepository) -> None:
        """Test loading real AISC data."""
        count = repository.load_all()
        # Should have at least the W shapes we generated
        assert count >= 200

    def test_get_real_section(self, repository: SectionsRepository) -> None:
        """Test getting a real AISC section."""
        section = repository.get("W14X30")
        assert section.name == "W14X30"
        assert section.shape == SectionShape.W
        assert section.A > 0
        assert section.Ix > 0
        assert section.d is not None
        assert section.d > 0

    def test_w_shapes_have_required_properties(self, repository: SectionsRepository) -> None:
        """Test that W shapes have all required properties."""
        w_shapes = repository.get_w_shapes()
        assert len(w_shapes) > 100  # Should have many W shapes

        for section in w_shapes:
            # All W shapes should have these properties
            assert section.A > 0
            assert section.Ix > 0
            assert section.Iy > 0
            assert section.d is not None
            assert section.bf is not None
            assert section.tw is not None
            assert section.tf is not None
            assert section.W is not None  # Weight

    def test_search_real_sections(self, repository: SectionsRepository) -> None:
        """Test searching real AISC sections."""
        # Search for W44 shapes (largest)
        results = repository.search("W44")
        assert len(results) >= 4

        # Search for common W14 shapes
        results = repository.search("W14X")
        assert len(results) >= 20
