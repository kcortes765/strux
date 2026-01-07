"""Tests for Section domain model."""

import pytest
from uuid import UUID

from paz.core.exceptions import ValidationError
from paz.domain.sections.section import (
    Section,
    SectionShape,
    SectionStandard,
    in_to_m,
    in2_to_m2,
    in3_to_m3,
    in4_to_m4,
    in6_to_m6,
    plf_to_kgm,
)


class TestSection:
    """Tests for Section dataclass."""

    def test_create_section_minimal(self) -> None:
        """Test creating a section with minimal required properties."""
        section = Section(
            name="W14X30",
            shape=SectionShape.W,
            A=0.00567,  # m²
            Ix=1.21e-4,  # m⁴
            Iy=8.14e-6,  # m⁴
        )
        assert section.name == "W14X30"
        assert section.shape == SectionShape.W
        assert section.A == 0.00567
        assert section.Ix == 1.21e-4
        assert section.Iy == 8.14e-6
        assert section.standard == SectionStandard.CUSTOM
        assert section.is_custom is False

    def test_create_section_full(self) -> None:
        """Test creating a section with all properties."""
        section = Section(
            name="W14X30",
            shape=SectionShape.W,
            standard=SectionStandard.AISC,
            A=0.00567,
            Ix=1.21e-4,
            Iy=8.14e-6,
            Sx=6.89e-4,
            Sy=9.54e-5,
            Zx=7.75e-4,
            Zy=1.47e-4,
            rx=0.146,
            ry=0.0378,
            J=1.52e-7,
            Cw=2.07e-9,
            d=0.351,
            bf=0.171,
            tw=0.00686,
            tf=0.00978,
            W=44.6,
            description="AISC W Shape",
            is_custom=False,
        )
        assert section.standard == SectionStandard.AISC
        assert section.Sx == 6.89e-4
        assert section.rx == 0.146
        assert section.J == 1.52e-7
        assert section.d == 0.351
        assert section.W == 44.6
        assert section.description == "AISC W Shape"

    def test_section_generates_uuid(self) -> None:
        """Test that section generates a UUID by default."""
        section = Section(
            name="Test",
            shape=SectionShape.CUSTOM,
            A=0.001,
            Ix=1e-6,
            Iy=1e-7,
        )
        assert isinstance(section.id, UUID)

    def test_invalid_area_raises_error(self) -> None:
        """Test that non-positive area raises ValidationError."""
        with pytest.raises(ValidationError, match="Area A must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=0,
                Ix=1e-6,
                Iy=1e-7,
            )

        with pytest.raises(ValidationError, match="Area A must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=-0.001,
                Ix=1e-6,
                Iy=1e-7,
            )

    def test_invalid_ix_raises_error(self) -> None:
        """Test that non-positive Ix raises ValidationError."""
        with pytest.raises(ValidationError, match="Moment of inertia Ix must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=0.001,
                Ix=0,
                Iy=1e-7,
            )

    def test_invalid_iy_raises_error(self) -> None:
        """Test that non-positive Iy raises ValidationError."""
        with pytest.raises(ValidationError, match="Moment of inertia Iy must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=0.001,
                Ix=1e-6,
                Iy=-1e-7,
            )

    def test_invalid_optional_properties(self) -> None:
        """Test that non-positive optional properties raise ValidationError."""
        with pytest.raises(ValidationError, match="Sx must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=0.001,
                Ix=1e-6,
                Iy=1e-7,
                Sx=0,
            )

        with pytest.raises(ValidationError, match="d must be positive"):
            Section(
                name="Invalid",
                shape=SectionShape.CUSTOM,
                A=0.001,
                Ix=1e-6,
                Iy=1e-7,
                d=-0.1,
            )

    def test_rx_calculated(self) -> None:
        """Test calculated radius of gyration about x-axis."""
        section = Section(
            name="Test",
            shape=SectionShape.CUSTOM,
            A=0.01,  # m²
            Ix=1e-4,  # m⁴
            Iy=1e-5,
        )
        # rx = sqrt(Ix/A) = sqrt(1e-4/0.01) = sqrt(0.01) = 0.1
        assert abs(section.rx_calculated - 0.1) < 1e-10

    def test_ry_calculated(self) -> None:
        """Test calculated radius of gyration about y-axis."""
        section = Section(
            name="Test",
            shape=SectionShape.CUSTOM,
            A=0.01,  # m²
            Ix=1e-4,
            Iy=2.5e-5,  # m⁴
        )
        # ry = sqrt(Iy/A) = sqrt(2.5e-5/0.01) = sqrt(0.0025) = 0.05
        assert abs(section.ry_calculated - 0.05) < 1e-10

    def test_rx_uses_provided_value(self) -> None:
        """Test that rx_calculated uses provided rx value."""
        section = Section(
            name="Test",
            shape=SectionShape.CUSTOM,
            A=0.01,
            Ix=1e-4,
            Iy=1e-5,
            rx=0.15,  # Provided value
        )
        assert section.rx_calculated == 0.15

    def test_to_dict(self) -> None:
        """Test serialization to dictionary."""
        section = Section(
            name="W14X30",
            shape=SectionShape.W,
            standard=SectionStandard.AISC,
            A=0.00567,
            Ix=1.21e-4,
            Iy=8.14e-6,
            d=0.351,
            description="Test section",
        )
        data = section.to_dict()

        assert data["name"] == "W14X30"
        assert data["shape"] == "W"
        assert data["standard"] == "AISC"
        assert data["A"] == 0.00567
        assert data["Ix"] == 1.21e-4
        assert data["Iy"] == 8.14e-6
        assert data["d"] == 0.351
        assert data["description"] == "Test section"
        assert "id" in data

    def test_from_dict(self) -> None:
        """Test deserialization from dictionary."""
        data = {
            "name": "W14X30",
            "shape": "W",
            "standard": "AISC",
            "A": 0.00567,
            "Ix": 1.21e-4,
            "Iy": 8.14e-6,
            "Sx": 6.89e-4,
            "d": 0.351,
            "description": "Test section",
        }
        section = Section.from_dict(data)

        assert section.name == "W14X30"
        assert section.shape == SectionShape.W
        assert section.standard == SectionStandard.AISC
        assert section.A == 0.00567
        assert section.Sx == 6.89e-4
        assert section.d == 0.351

    def test_from_dict_with_id(self) -> None:
        """Test deserialization preserves ID if provided."""
        test_id = "12345678-1234-5678-1234-567812345678"
        data = {
            "id": test_id,
            "name": "Test",
            "shape": "CUSTOM",
            "A": 0.001,
            "Ix": 1e-6,
            "Iy": 1e-7,
        }
        section = Section.from_dict(data)
        assert str(section.id) == test_id

    def test_copy(self) -> None:
        """Test copying a section."""
        original = Section(
            name="W14X30",
            shape=SectionShape.W,
            standard=SectionStandard.AISC,
            A=0.00567,
            Ix=1.21e-4,
            Iy=8.14e-6,
        )
        copy = original.copy()

        assert copy.name == "W14X30 (copy)"
        assert copy.id != original.id
        assert copy.A == original.A
        assert copy.standard == SectionStandard.CUSTOM
        assert copy.is_custom is True

    def test_copy_with_new_name(self) -> None:
        """Test copying a section with a new name."""
        original = Section(
            name="W14X30",
            shape=SectionShape.W,
            A=0.00567,
            Ix=1.21e-4,
            Iy=8.14e-6,
        )
        copy = original.copy(new_name="Custom W14")
        assert copy.name == "Custom W14"


class TestSectionShape:
    """Tests for SectionShape enum."""

    def test_all_shapes_exist(self) -> None:
        """Test that all expected shapes exist."""
        shapes = [
            SectionShape.W,
            SectionShape.HP,
            SectionShape.M,
            SectionShape.S,
            SectionShape.C,
            SectionShape.MC,
            SectionShape.L,
            SectionShape.WT,
            SectionShape.MT,
            SectionShape.ST,
            SectionShape.HSS_RECT,
            SectionShape.HSS_ROUND,
            SectionShape.PIPE,
            SectionShape.DOUBLE_L,
            SectionShape.CUSTOM,
        ]
        assert len(shapes) == 15

    def test_shape_values(self) -> None:
        """Test shape string values."""
        assert SectionShape.W.value == "W"
        assert SectionShape.HSS_RECT.value == "HSS_RECT"
        assert SectionShape.DOUBLE_L.value == "2L"


class TestSectionStandard:
    """Tests for SectionStandard enum."""

    def test_all_standards_exist(self) -> None:
        """Test that all expected standards exist."""
        standards = [
            SectionStandard.AISC,
            SectionStandard.EUROCODE,
            SectionStandard.NCH,
            SectionStandard.CUSTOM,
        ]
        assert len(standards) == 4


class TestUnitConversions:
    """Tests for unit conversion helpers."""

    def test_in_to_m(self) -> None:
        """Test inches to meters conversion."""
        assert abs(in_to_m(1) - 0.0254) < 1e-10
        assert abs(in_to_m(12) - 0.3048) < 1e-10  # 1 foot

    def test_in2_to_m2(self) -> None:
        """Test square inches to square meters."""
        assert abs(in2_to_m2(1) - 0.00064516) < 1e-10

    def test_in3_to_m3(self) -> None:
        """Test cubic inches to cubic meters."""
        assert abs(in3_to_m3(1) - 1.6387064e-5) < 1e-12

    def test_in4_to_m4(self) -> None:
        """Test in⁴ to m⁴."""
        assert abs(in4_to_m4(1) - 4.162314e-7) < 1e-13

    def test_in6_to_m6(self) -> None:
        """Test in⁶ to m⁶."""
        assert abs(in6_to_m6(1) - 2.6839e-10) < 1e-14

    def test_plf_to_kgm(self) -> None:
        """Test pounds per foot to kg/m."""
        assert abs(plf_to_kgm(1) - 1.48816) < 1e-5
