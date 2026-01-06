"""
Restraint (boundary condition) model for structural nodes.

Defines which degrees of freedom are fixed at a node.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Restraint:
    """
    Represents boundary conditions at a node.

    Each boolean indicates whether that degree of freedom is restrained (fixed).
    True = fixed, False = free.

    Attributes:
        ux: Translation in X direction
        uy: Translation in Y direction
        uz: Translation in Z direction
        rx: Rotation about X axis
        ry: Rotation about Y axis
        rz: Rotation about Z axis
    """

    ux: bool = False
    uy: bool = False
    uz: bool = False
    rx: bool = False
    ry: bool = False
    rz: bool = False

    @property
    def is_free(self) -> bool:
        """Check if all degrees of freedom are free."""
        return not any([self.ux, self.uy, self.uz, self.rx, self.ry, self.rz])

    @property
    def is_fixed(self) -> bool:
        """Check if all degrees of freedom are fixed."""
        return all([self.ux, self.uy, self.uz, self.rx, self.ry, self.rz])

    @property
    def is_pinned(self) -> bool:
        """Check if translations are fixed but rotations are free."""
        return (
            self.ux
            and self.uy
            and self.uz
            and not self.rx
            and not self.ry
            and not self.rz
        )

    def to_list(self) -> list[bool]:
        """Convert to list [ux, uy, uz, rx, ry, rz]."""
        return [self.ux, self.uy, self.uz, self.rx, self.ry, self.rz]

    def to_int_list(self) -> list[int]:
        """Convert to integer list (1=fixed, 0=free) for OpenSees."""
        return [int(v) for v in self.to_list()]

    def to_dict(self) -> dict[str, bool]:
        """Convert to dictionary for serialization."""
        return {
            "ux": self.ux,
            "uy": self.uy,
            "uz": self.uz,
            "rx": self.rx,
            "ry": self.ry,
            "rz": self.rz,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Restraint":
        """Create from dictionary."""
        return cls(
            ux=bool(data.get("ux", False)),
            uy=bool(data.get("uy", False)),
            uz=bool(data.get("uz", False)),
            rx=bool(data.get("rx", False)),
            ry=bool(data.get("ry", False)),
            rz=bool(data.get("rz", False)),
        )

    @classmethod
    def from_list(cls, values: list[bool | int]) -> "Restraint":
        """Create from list [ux, uy, uz, rx, ry, rz]."""
        if len(values) != 6:
            msg = f"Expected 6 values, got {len(values)}"
            raise ValueError(msg)
        return cls(
            ux=bool(values[0]),
            uy=bool(values[1]),
            uz=bool(values[2]),
            rx=bool(values[3]),
            ry=bool(values[4]),
            rz=bool(values[5]),
        )


# Common restraint presets
FREE = Restraint()
FIXED = Restraint(ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)
PINNED = Restraint(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)
ROLLER_X = Restraint(ux=False, uy=True, uz=True, rx=False, ry=False, rz=False)
ROLLER_Y = Restraint(ux=True, uy=False, uz=True, rx=False, ry=False, rz=False)
ROLLER_Z = Restraint(ux=True, uy=True, uz=False, rx=False, ry=False, rz=False)
