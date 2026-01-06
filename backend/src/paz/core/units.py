"""
Unit system and conversion utilities for PAZ.

Supports multiple unit systems commonly used in structural engineering:
- SI (m, kN)
- Imperial (ft, kip)
- Mixed variations
"""

from dataclasses import dataclass
from enum import Enum
from typing import Final

from paz.core.exceptions import UnitConversionError


class LengthUnit(str, Enum):
    """Length units supported by PAZ."""

    METER = "m"
    CENTIMETER = "cm"
    MILLIMETER = "mm"
    FOOT = "ft"
    INCH = "in"


class ForceUnit(str, Enum):
    """Force units supported by PAZ."""

    KILONEWTON = "kN"
    NEWTON = "N"
    KILOGRAM_FORCE = "kgf"
    TON_FORCE = "tonf"
    KIP = "kip"
    POUND_FORCE = "lbf"


class AngleUnit(str, Enum):
    """Angle units supported by PAZ."""

    DEGREE = "deg"
    RADIAN = "rad"


@dataclass(frozen=True)
class UnitSystem:
    """
    Defines the unit system for a project.

    Attributes:
        length: Length unit (default: meters)
        force: Force unit (default: kilonewtons)
        angle: Angle unit (default: degrees)
    """

    length: LengthUnit = LengthUnit.METER
    force: ForceUnit = ForceUnit.KILONEWTON
    angle: AngleUnit = AngleUnit.DEGREE

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for serialization."""
        return {
            "length": self.length.value,
            "force": self.force.value,
            "angle": self.angle.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "UnitSystem":
        """Create from dictionary."""
        return cls(
            length=LengthUnit(data.get("length", "m")),
            force=ForceUnit(data.get("force", "kN")),
            angle=AngleUnit(data.get("angle", "deg")),
        )


# Predefined unit systems
SI_UNITS: Final[UnitSystem] = UnitSystem(
    length=LengthUnit.METER,
    force=ForceUnit.KILONEWTON,
    angle=AngleUnit.DEGREE,
)

IMPERIAL_UNITS: Final[UnitSystem] = UnitSystem(
    length=LengthUnit.FOOT,
    force=ForceUnit.KIP,
    angle=AngleUnit.DEGREE,
)


# Conversion factors to base units (meter, newton, radian)
_LENGTH_TO_METER: Final[dict[LengthUnit, float]] = {
    LengthUnit.METER: 1.0,
    LengthUnit.CENTIMETER: 0.01,
    LengthUnit.MILLIMETER: 0.001,
    LengthUnit.FOOT: 0.3048,
    LengthUnit.INCH: 0.0254,
}

_FORCE_TO_NEWTON: Final[dict[ForceUnit, float]] = {
    ForceUnit.NEWTON: 1.0,
    ForceUnit.KILONEWTON: 1000.0,
    ForceUnit.KILOGRAM_FORCE: 9.80665,
    ForceUnit.TON_FORCE: 9806.65,
    ForceUnit.KIP: 4448.2216,
    ForceUnit.POUND_FORCE: 4.4482216,
}

_ANGLE_TO_RADIAN: Final[dict[AngleUnit, float]] = {
    AngleUnit.RADIAN: 1.0,
    AngleUnit.DEGREE: 0.017453292519943295,  # pi / 180
}


def convert_length(value: float, from_unit: LengthUnit, to_unit: LengthUnit) -> float:
    """
    Convert a length value between units.

    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit

    Returns:
        Converted value

    Raises:
        UnitConversionError: If conversion fails
    """
    if from_unit == to_unit:
        return value

    try:
        # Convert to meters, then to target unit
        meters = value * _LENGTH_TO_METER[from_unit]
        return meters / _LENGTH_TO_METER[to_unit]
    except KeyError as e:
        raise UnitConversionError(
            f"Unknown length unit: {e}",
            from_unit=from_unit.value,
            to_unit=to_unit.value,
        ) from e


def convert_force(value: float, from_unit: ForceUnit, to_unit: ForceUnit) -> float:
    """
    Convert a force value between units.

    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit

    Returns:
        Converted value

    Raises:
        UnitConversionError: If conversion fails
    """
    if from_unit == to_unit:
        return value

    try:
        # Convert to newtons, then to target unit
        newtons = value * _FORCE_TO_NEWTON[from_unit]
        return newtons / _FORCE_TO_NEWTON[to_unit]
    except KeyError as e:
        raise UnitConversionError(
            f"Unknown force unit: {e}",
            from_unit=from_unit.value,
            to_unit=to_unit.value,
        ) from e


def convert_angle(value: float, from_unit: AngleUnit, to_unit: AngleUnit) -> float:
    """
    Convert an angle value between units.

    Args:
        value: The value to convert
        from_unit: Source unit
        to_unit: Target unit

    Returns:
        Converted value

    Raises:
        UnitConversionError: If conversion fails
    """
    if from_unit == to_unit:
        return value

    try:
        # Convert to radians, then to target unit
        radians = value * _ANGLE_TO_RADIAN[from_unit]
        return radians / _ANGLE_TO_RADIAN[to_unit]
    except KeyError as e:
        raise UnitConversionError(
            f"Unknown angle unit: {e}",
            from_unit=from_unit.value,
            to_unit=to_unit.value,
        ) from e


class UnitConverter:
    """
    Utility class for converting values between unit systems.

    Example:
        converter = UnitConverter(from_system=SI_UNITS, to_system=IMPERIAL_UNITS)
        length_ft = converter.length(10.0)  # 10 m -> 32.808 ft
        force_kip = converter.force(100.0)  # 100 kN -> 22.48 kip
    """

    def __init__(self, from_system: UnitSystem, to_system: UnitSystem) -> None:
        self.from_system = from_system
        self.to_system = to_system

    def length(self, value: float) -> float:
        """Convert length value between systems."""
        return convert_length(value, self.from_system.length, self.to_system.length)

    def force(self, value: float) -> float:
        """Convert force value between systems."""
        return convert_force(value, self.from_system.force, self.to_system.force)

    def angle(self, value: float) -> float:
        """Convert angle value between systems."""
        return convert_angle(value, self.from_system.angle, self.to_system.angle)

    def stress(self, value: float) -> float:
        """Convert stress (force/area) value between systems."""
        # Stress = Force / Length^2
        force_factor = _FORCE_TO_NEWTON[self.from_system.force] / _FORCE_TO_NEWTON[
            self.to_system.force
        ]
        length_factor = _LENGTH_TO_METER[self.from_system.length] / _LENGTH_TO_METER[
            self.to_system.length
        ]
        return value * force_factor / (length_factor**2)

    def moment(self, value: float) -> float:
        """Convert moment (force * length) value between systems."""
        force_factor = _FORCE_TO_NEWTON[self.from_system.force] / _FORCE_TO_NEWTON[
            self.to_system.force
        ]
        length_factor = _LENGTH_TO_METER[self.from_system.length] / _LENGTH_TO_METER[
            self.to_system.length
        ]
        return value * force_factor * length_factor
