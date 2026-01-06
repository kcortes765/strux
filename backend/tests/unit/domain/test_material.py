"""Tests for Material model."""

import pytest

from paz.core.exceptions import ValidationError
from paz.domain.materials.material import (
    Material,
    MaterialStandard,
    MaterialType,
    mpa_to_kpa,
    ksi_to_kpa,
)


class TestMaterial:
    """Tests for Material dataclass."""

    def test_create_steel_material(self) -> None:
        """Create a basic steel material."""
        steel = Material(
            name="A36",
            material_type=MaterialType.STEEL,
            E=200_000_000,  # 200 GPa in kPa
            nu=0.3,
            rho=7850,
            fy=250_000,  # 250 MPa in kPa
            fu=400_000,  # 400 MPa in kPa
        )
        assert steel.name == "A36"
        assert steel.material_type == MaterialType.STEEL
        assert steel.E == 200_000_000
        assert steel.nu == 0.3
        assert steel.rho == 7850

    def test_create_concrete_material(self) -> None:
        """Create a basic concrete material."""
        concrete = Material(
            name="H30",
            material_type=MaterialType.CONCRETE,
            E=25_743_000,
            nu=0.2,
            rho=2400,
            fc=30_000,  # 30 MPa in kPa
        )
        assert concrete.name == "H30"
        assert concrete.material_type == MaterialType.CONCRETE
        assert concrete.fc == 30_000

    def test_shear_modulus_calculation(self) -> None:
        """G should be calculated from E and nu."""
        material = Material(
            name="Test",
            material_type=MaterialType.STEEL,
            E=200_000_000,
            nu=0.3,
            rho=7850,
        )
        # G = E / (2 * (1 + nu)) = 200000000 / (2 * 1.3) = 76923076.92
        expected_g = 200_000_000 / (2 * 1.3)
        assert abs(material.G - expected_g) < 1

    def test_bulk_modulus_calculation(self) -> None:
        """K should be calculated from E and nu."""
        material = Material(
            name="Test",
            material_type=MaterialType.STEEL,
            E=200_000_000,
            nu=0.3,
            rho=7850,
        )
        # K = E / (3 * (1 - 2*nu)) = 200000000 / (3 * 0.4) = 166666666.67
        expected_k = 200_000_000 / (3 * 0.4)
        assert abs(material.K - expected_k) < 1

    def test_validation_negative_E(self) -> None:
        """Negative E should raise ValidationError."""
        with pytest.raises(ValidationError, match="E must be positive"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=-100,
                nu=0.3,
                rho=7850,
            )

    def test_validation_zero_E(self) -> None:
        """Zero E should raise ValidationError."""
        with pytest.raises(ValidationError, match="E must be positive"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=0,
                nu=0.3,
                rho=7850,
            )

    def test_validation_nu_out_of_range_high(self) -> None:
        """nu > 0.5 should raise ValidationError."""
        with pytest.raises(ValidationError, match="nu must be between"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=200_000_000,
                nu=0.6,
                rho=7850,
            )

    def test_validation_nu_out_of_range_low(self) -> None:
        """nu < 0 should raise ValidationError."""
        with pytest.raises(ValidationError, match="nu must be between"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=200_000_000,
                nu=-0.1,
                rho=7850,
            )

    def test_validation_negative_rho(self) -> None:
        """Negative rho should raise ValidationError."""
        with pytest.raises(ValidationError, match="rho must be positive"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=200_000_000,
                nu=0.3,
                rho=-100,
            )

    def test_validation_negative_fy(self) -> None:
        """Negative fy should raise ValidationError."""
        with pytest.raises(ValidationError, match="fy must be positive"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=200_000_000,
                nu=0.3,
                rho=7850,
                fy=-250_000,
            )

    def test_validation_fu_less_than_fy(self) -> None:
        """fu < fy should raise ValidationError."""
        with pytest.raises(ValidationError, match="fu.*should be >= yield strength"):
            Material(
                name="Invalid",
                material_type=MaterialType.STEEL,
                E=200_000_000,
                nu=0.3,
                rho=7850,
                fy=350_000,
                fu=250_000,  # Less than fy
            )

    def test_to_dict_from_dict_roundtrip(self) -> None:
        """Serialization roundtrip should preserve data."""
        original = Material(
            name="A992",
            material_type=MaterialType.STEEL,
            standard=MaterialStandard.ASTM,
            E=200_000_000,
            nu=0.3,
            rho=7850,
            fy=345_000,
            fu=450_000,
            description="Test material",
        )
        restored = Material.from_dict(original.to_dict())
        assert restored.name == original.name
        assert restored.material_type == original.material_type
        assert restored.E == original.E
        assert restored.fy == original.fy

    def test_copy_creates_custom_material(self) -> None:
        """copy should create a custom material with new ID."""
        original = Material(
            name="A36",
            material_type=MaterialType.STEEL,
            standard=MaterialStandard.ASTM,
            E=200_000_000,
            nu=0.3,
            rho=7850,
            fy=250_000,
            fu=400_000,
        )
        copied = original.copy("A36-Modified")
        assert copied.name == "A36-Modified"
        assert copied.id != original.id
        assert copied.is_custom is True
        assert copied.standard == MaterialStandard.CUSTOM
        assert copied.E == original.E

    def test_copy_without_name(self) -> None:
        """copy without name should append (copy)."""
        original = Material(
            name="A36",
            material_type=MaterialType.STEEL,
            E=200_000_000,
            nu=0.3,
            rho=7850,
        )
        copied = original.copy()
        assert copied.name == "A36 (copy)"


class TestUnitConversions:
    """Tests for unit conversion helpers."""

    def test_mpa_to_kpa(self) -> None:
        """MPa to kPa conversion."""
        assert mpa_to_kpa(1) == 1000
        assert mpa_to_kpa(250) == 250_000

    def test_ksi_to_kpa(self) -> None:
        """ksi to kPa conversion."""
        # 1 ksi = 6894.76 kPa
        assert abs(ksi_to_kpa(1) - 6894.76) < 0.01
        assert abs(ksi_to_kpa(50) - 344_738) < 1
