"""
Section model for structural analysis.

Defines cross-section properties for structural elements (beams, columns).
Properties follow AISC notation and SI units (m, m², m⁴).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from paz.core.exceptions import ValidationError


class SectionShape(str, Enum):
    """Types of cross-section shapes."""

    W = "W"  # Wide Flange
    HP = "HP"  # H-Pile
    M = "M"  # Miscellaneous
    S = "S"  # American Standard Beam
    C = "C"  # Channel
    MC = "MC"  # Miscellaneous Channel
    L = "L"  # Angle (single)
    WT = "WT"  # Tee (cut from W)
    MT = "MT"  # Tee (cut from M)
    ST = "ST"  # Tee (cut from S)
    HSS_RECT = "HSS_RECT"  # Hollow Structural Section - Rectangular
    HSS_ROUND = "HSS_ROUND"  # Hollow Structural Section - Round
    PIPE = "PIPE"  # Pipe
    DOUBLE_L = "2L"  # Double Angle
    CUSTOM = "CUSTOM"  # User-defined


class SectionStandard(str, Enum):
    """Section standards/codes."""

    AISC = "AISC"
    EUROCODE = "Eurocode"
    NCH = "NCh"
    CUSTOM = "Custom"


@dataclass
class Section:
    """
    Represents a structural cross-section with geometric properties.

    All dimensional properties use SI units:
    - Lengths: meters (m)
    - Areas: square meters (m²)
    - Moments of inertia: m⁴
    - Section moduli: m³
    - Torsional constant: m⁴
    - Warping constant: m⁶

    Attributes:
        id: Unique identifier
        name: Section designation (e.g., "W14X30", "HSS8X4X1/2")
        shape: Section shape type
        standard: Section standard/code

        # Area properties
        A: Cross-sectional area (m²)

        # Moments of inertia
        Ix: Moment of inertia about x-axis (strong axis) (m⁴)
        Iy: Moment of inertia about y-axis (weak axis) (m⁴)

        # Section moduli (elastic)
        Sx: Elastic section modulus about x-axis (m³)
        Sy: Elastic section modulus about y-axis (m³)

        # Plastic section moduli
        Zx: Plastic section modulus about x-axis (m³)
        Zy: Plastic section modulus about y-axis (m³)

        # Radii of gyration
        rx: Radius of gyration about x-axis (m)
        ry: Radius of gyration about y-axis (m)

        # Torsional properties
        J: Torsional constant (m⁴)
        Cw: Warping constant (m⁶)

        # Dimensional properties (for W, C, L shapes)
        d: Overall depth (m)
        bf: Flange width (m)
        tw: Web thickness (m)
        tf: Flange thickness (m)

        # For HSS and pipes
        t: Wall thickness (m)
        OD: Outside diameter (m) - for round sections

        # Weight
        W: Weight per unit length (kg/m)

        description: Optional description
        is_custom: Whether this is a user-defined section
    """

    name: str
    shape: SectionShape
    A: float  # Area (m²)
    Ix: float  # Moment of inertia x (m⁴)
    Iy: float  # Moment of inertia y (m⁴)
    id: UUID = field(default_factory=uuid4)
    standard: SectionStandard = SectionStandard.CUSTOM

    # Elastic section moduli
    Sx: float | None = None  # m³
    Sy: float | None = None  # m³

    # Plastic section moduli
    Zx: float | None = None  # m³
    Zy: float | None = None  # m³

    # Radii of gyration
    rx: float | None = None  # m
    ry: float | None = None  # m

    # Torsional properties
    J: float | None = None  # m⁴
    Cw: float | None = None  # m⁶

    # Dimensional properties
    d: float | None = None  # depth (m)
    bf: float | None = None  # flange width (m)
    tw: float | None = None  # web thickness (m)
    tf: float | None = None  # flange thickness (m)
    t: float | None = None  # wall thickness (m)
    OD: float | None = None  # outside diameter (m)

    # Weight
    W: float | None = None  # kg/m

    description: str = ""
    is_custom: bool = False

    def __post_init__(self) -> None:
        """Validate section properties."""
        self._validate()

    def _validate(self) -> None:
        """Validate section properties."""
        if self.A <= 0:
            raise ValidationError(
                f"Area A must be positive, got {self.A}",
                field="A",
            )

        if self.Ix <= 0:
            raise ValidationError(
                f"Moment of inertia Ix must be positive, got {self.Ix}",
                field="Ix",
            )

        if self.Iy <= 0:
            raise ValidationError(
                f"Moment of inertia Iy must be positive, got {self.Iy}",
                field="Iy",
            )

        # Validate optional positive properties
        positive_fields = ["Sx", "Sy", "Zx", "Zy", "rx", "ry", "J", "Cw", "d", "bf", "tw", "tf", "t", "OD", "W"]
        for field_name in positive_fields:
            value = getattr(self, field_name)
            if value is not None and value <= 0:
                raise ValidationError(
                    f"{field_name} must be positive, got {value}",
                    field=field_name,
                )

    @property
    def rx_calculated(self) -> float:
        """Calculate radius of gyration about x-axis if not provided."""
        if self.rx is not None:
            return self.rx
        return float((self.Ix / self.A) ** 0.5)

    @property
    def ry_calculated(self) -> float:
        """Calculate radius of gyration about y-axis if not provided."""
        if self.ry is not None:
            return self.ry
        return float((self.Iy / self.A) ** 0.5)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "shape": self.shape.value,
            "standard": self.standard.value,
            "A": self.A,
            "Ix": self.Ix,
            "Iy": self.Iy,
            "Sx": self.Sx,
            "Sy": self.Sy,
            "Zx": self.Zx,
            "Zy": self.Zy,
            "rx": self.rx,
            "ry": self.ry,
            "J": self.J,
            "Cw": self.Cw,
            "d": self.d,
            "bf": self.bf,
            "tw": self.tw,
            "tf": self.tf,
            "t": self.t,
            "OD": self.OD,
            "W": self.W,
            "description": self.description,
            "is_custom": self.is_custom,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Section":
        """Create from dictionary."""
        return cls(
            id=UUID(data["id"]) if "id" in data else uuid4(),
            name=data["name"],
            shape=SectionShape(data.get("shape", "CUSTOM")),
            standard=SectionStandard(data.get("standard", "Custom")),
            A=float(data["A"]),
            Ix=float(data["Ix"]),
            Iy=float(data["Iy"]),
            Sx=float(data["Sx"]) if data.get("Sx") is not None else None,
            Sy=float(data["Sy"]) if data.get("Sy") is not None else None,
            Zx=float(data["Zx"]) if data.get("Zx") is not None else None,
            Zy=float(data["Zy"]) if data.get("Zy") is not None else None,
            rx=float(data["rx"]) if data.get("rx") is not None else None,
            ry=float(data["ry"]) if data.get("ry") is not None else None,
            J=float(data["J"]) if data.get("J") is not None else None,
            Cw=float(data["Cw"]) if data.get("Cw") is not None else None,
            d=float(data["d"]) if data.get("d") is not None else None,
            bf=float(data["bf"]) if data.get("bf") is not None else None,
            tw=float(data["tw"]) if data.get("tw") is not None else None,
            tf=float(data["tf"]) if data.get("tf") is not None else None,
            t=float(data["t"]) if data.get("t") is not None else None,
            OD=float(data["OD"]) if data.get("OD") is not None else None,
            W=float(data["W"]) if data.get("W") is not None else None,
            description=data.get("description", ""),
            is_custom=data.get("is_custom", False),
        )

    def copy(self, new_name: str | None = None) -> "Section":
        """
        Create a copy of this section.

        Args:
            new_name: Optional new name for the copy

        Returns:
            New Section instance with same properties but new ID
        """
        return Section(
            id=uuid4(),
            name=new_name if new_name is not None else f"{self.name} (copy)",
            shape=self.shape,
            standard=SectionStandard.CUSTOM,
            A=self.A,
            Ix=self.Ix,
            Iy=self.Iy,
            Sx=self.Sx,
            Sy=self.Sy,
            Zx=self.Zx,
            Zy=self.Zy,
            rx=self.rx,
            ry=self.ry,
            J=self.J,
            Cw=self.Cw,
            d=self.d,
            bf=self.bf,
            tw=self.tw,
            tf=self.tf,
            t=self.t,
            OD=self.OD,
            W=self.W,
            description=self.description,
            is_custom=True,
        )


# Unit conversion helpers (AISC uses imperial, we store in SI)
def in2_to_m2(in2: float) -> float:
    """Convert square inches to square meters."""
    return in2 * 0.00064516


def in4_to_m4(in4: float) -> float:
    """Convert in⁴ to m⁴."""
    return in4 * 4.162314e-7


def in6_to_m6(in6: float) -> float:
    """Convert in⁶ to m⁶."""
    return in6 * 2.6839e-10


def in3_to_m3(in3: float) -> float:
    """Convert in³ to m³."""
    return in3 * 1.6387064e-5


def in_to_m(inches: float) -> float:
    """Convert inches to meters."""
    return inches * 0.0254


def plf_to_kgm(plf: float) -> float:
    """Convert pounds per linear foot to kg/m."""
    return plf * 1.48816
