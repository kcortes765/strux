"""Tests for unit conversion utilities."""

import pytest
from math import isclose

from paz.core.units import (
    LengthUnit,
    ForceUnit,
    AngleUnit,
    UnitSystem,
    SI_UNITS,
    IMPERIAL_UNITS,
    convert_length,
    convert_force,
    convert_angle,
    UnitConverter,
)


class TestLengthConversion:
    """Tests for length unit conversions."""

    def test_same_unit_no_conversion(self) -> None:
        """Converting to the same unit should return the same value."""
        assert convert_length(10.0, LengthUnit.METER, LengthUnit.METER) == 10.0

    def test_meters_to_feet(self) -> None:
        """1 meter = 3.28084 feet."""
        result = convert_length(1.0, LengthUnit.METER, LengthUnit.FOOT)
        assert isclose(result, 3.28084, rel_tol=1e-4)

    def test_feet_to_meters(self) -> None:
        """1 foot = 0.3048 meters."""
        result = convert_length(1.0, LengthUnit.FOOT, LengthUnit.METER)
        assert isclose(result, 0.3048, rel_tol=1e-6)

    def test_meters_to_millimeters(self) -> None:
        """1 meter = 1000 millimeters."""
        result = convert_length(1.0, LengthUnit.METER, LengthUnit.MILLIMETER)
        assert result == 1000.0

    def test_inches_to_centimeters(self) -> None:
        """1 inch = 2.54 centimeters."""
        result = convert_length(1.0, LengthUnit.INCH, LengthUnit.CENTIMETER)
        assert isclose(result, 2.54, rel_tol=1e-6)


class TestForceConversion:
    """Tests for force unit conversions."""

    def test_same_unit_no_conversion(self) -> None:
        """Converting to the same unit should return the same value."""
        assert convert_force(100.0, ForceUnit.KILONEWTON, ForceUnit.KILONEWTON) == 100.0

    def test_kn_to_kip(self) -> None:
        """1 kN = 0.2248 kip."""
        result = convert_force(1.0, ForceUnit.KILONEWTON, ForceUnit.KIP)
        assert isclose(result, 0.2248, rel_tol=1e-3)

    def test_kip_to_kn(self) -> None:
        """1 kip = 4.4482 kN."""
        result = convert_force(1.0, ForceUnit.KIP, ForceUnit.KILONEWTON)
        assert isclose(result, 4.4482, rel_tol=1e-3)

    def test_kn_to_tonf(self) -> None:
        """1 kN = 0.10197 tonf."""
        result = convert_force(1.0, ForceUnit.KILONEWTON, ForceUnit.TON_FORCE)
        assert isclose(result, 0.10197, rel_tol=1e-3)

    def test_kn_to_newton(self) -> None:
        """1 kN = 1000 N."""
        result = convert_force(1.0, ForceUnit.KILONEWTON, ForceUnit.NEWTON)
        assert result == 1000.0


class TestAngleConversion:
    """Tests for angle unit conversions."""

    def test_degrees_to_radians(self) -> None:
        """180 degrees = pi radians."""
        import math

        result = convert_angle(180.0, AngleUnit.DEGREE, AngleUnit.RADIAN)
        assert isclose(result, math.pi, rel_tol=1e-9)

    def test_radians_to_degrees(self) -> None:
        """pi radians = 180 degrees."""
        import math

        result = convert_angle(math.pi, AngleUnit.RADIAN, AngleUnit.DEGREE)
        assert isclose(result, 180.0, rel_tol=1e-9)


class TestUnitSystem:
    """Tests for UnitSystem dataclass."""

    def test_default_is_si(self) -> None:
        """Default unit system should be SI."""
        system = UnitSystem()
        assert system.length == LengthUnit.METER
        assert system.force == ForceUnit.KILONEWTON
        assert system.angle == AngleUnit.DEGREE

    def test_to_dict(self) -> None:
        """Unit system should serialize to dict correctly."""
        result = SI_UNITS.to_dict()
        assert result == {"length": "m", "force": "kN", "angle": "deg"}

    def test_from_dict(self) -> None:
        """Unit system should deserialize from dict correctly."""
        data = {"length": "ft", "force": "kip", "angle": "deg"}
        system = UnitSystem.from_dict(data)
        assert system.length == LengthUnit.FOOT
        assert system.force == ForceUnit.KIP

    def test_imperial_units(self) -> None:
        """Imperial units should be ft/kip."""
        assert IMPERIAL_UNITS.length == LengthUnit.FOOT
        assert IMPERIAL_UNITS.force == ForceUnit.KIP


class TestUnitConverter:
    """Tests for UnitConverter class."""

    def test_si_to_imperial_length(self) -> None:
        """Convert 10 meters to feet."""
        converter = UnitConverter(SI_UNITS, IMPERIAL_UNITS)
        result = converter.length(10.0)
        assert isclose(result, 32.8084, rel_tol=1e-4)

    def test_si_to_imperial_force(self) -> None:
        """Convert 100 kN to kip."""
        converter = UnitConverter(SI_UNITS, IMPERIAL_UNITS)
        result = converter.force(100.0)
        assert isclose(result, 22.48, rel_tol=1e-2)

    def test_imperial_to_si_roundtrip(self) -> None:
        """Converting there and back should return original value."""
        to_imperial = UnitConverter(SI_UNITS, IMPERIAL_UNITS)
        to_si = UnitConverter(IMPERIAL_UNITS, SI_UNITS)

        original = 15.5
        imperial = to_imperial.length(original)
        back = to_si.length(imperial)

        assert isclose(back, original, rel_tol=1e-9)
