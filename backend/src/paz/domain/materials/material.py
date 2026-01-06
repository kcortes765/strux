"""
Material model for structural analysis.

Defines material properties for steel, concrete, and other structural materials.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from paz.core.exceptions import ValidationError


class MaterialType(str, Enum):
    """Types of structural materials."""

    STEEL = "steel"
    CONCRETE = "concrete"
    ALUMINUM = "aluminum"
    WOOD = "wood"
    MASONRY = "masonry"
    OTHER = "other"


class MaterialStandard(str, Enum):
    """Material standards/codes."""

    ASTM = "ASTM"
    NCH = "NCh"
    EUROCODE = "Eurocode"
    AISC = "AISC"
    ACI = "ACI"
    CUSTOM = "Custom"


@dataclass
class Material:
    """
    Represents a structural material with mechanical properties.

    Attributes:
        id: Unique identifier
        name: Material name (e.g., "A36", "H30")
        material_type: Type of material (steel, concrete, etc.)
        standard: Material standard/code
        E: Elastic modulus (Young's modulus) in kN/m² (kPa)
        nu: Poisson's ratio (dimensionless, 0 to 0.5)
        rho: Density in kg/m³
        fy: Yield strength in kN/m² (kPa) - for steel
        fu: Ultimate strength in kN/m² (kPa) - for steel
        fc: Compressive strength in kN/m² (kPa) - for concrete
        description: Optional description
        is_custom: Whether this is a user-defined material
    """

    name: str
    material_type: MaterialType
    E: float  # Elastic modulus (kPa)
    nu: float  # Poisson's ratio
    rho: float  # Density (kg/m³)
    id: UUID = field(default_factory=uuid4)
    standard: MaterialStandard = MaterialStandard.CUSTOM
    fy: float | None = None  # Yield strength (kPa)
    fu: float | None = None  # Ultimate strength (kPa)
    fc: float | None = None  # Compressive strength (kPa)
    description: str = ""
    is_custom: bool = False

    def __post_init__(self) -> None:
        """Validate material properties."""
        self._validate()

    def _validate(self) -> None:
        """Validate material properties."""
        # Elastic modulus must be positive
        if self.E <= 0:
            raise ValidationError(
                f"Elastic modulus E must be positive, got {self.E}",
                field="E",
            )

        # Poisson's ratio must be between 0 and 0.5
        if not 0 <= self.nu <= 0.5:
            raise ValidationError(
                f"Poisson's ratio nu must be between 0 and 0.5, got {self.nu}",
                field="nu",
            )

        # Density must be positive
        if self.rho <= 0:
            raise ValidationError(
                f"Density rho must be positive, got {self.rho}",
                field="rho",
            )

        # Yield strength must be positive if specified
        if self.fy is not None and self.fy <= 0:
            raise ValidationError(
                f"Yield strength fy must be positive, got {self.fy}",
                field="fy",
            )

        # Ultimate strength must be positive if specified
        if self.fu is not None and self.fu <= 0:
            raise ValidationError(
                f"Ultimate strength fu must be positive, got {self.fu}",
                field="fu",
            )

        # Compressive strength must be positive if specified
        if self.fc is not None and self.fc <= 0:
            raise ValidationError(
                f"Compressive strength fc must be positive, got {self.fc}",
                field="fc",
            )

        # fu should be >= fy for steel
        if self.fy is not None and self.fu is not None and self.fu < self.fy:
            raise ValidationError(
                f"Ultimate strength fu ({self.fu}) should be >= yield strength fy ({self.fy})",
                field="fu",
            )

    @property
    def G(self) -> float:
        """
        Calculate shear modulus from E and nu.

        G = E / (2 * (1 + nu))
        """
        return self.E / (2 * (1 + self.nu))

    @property
    def K(self) -> float:
        """
        Calculate bulk modulus from E and nu.

        K = E / (3 * (1 - 2*nu))
        """
        if self.nu == 0.5:
            return float("inf")  # Incompressible material
        return self.E / (3 * (1 - 2 * self.nu))

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "material_type": self.material_type.value,
            "standard": self.standard.value,
            "E": self.E,
            "nu": self.nu,
            "rho": self.rho,
            "fy": self.fy,
            "fu": self.fu,
            "fc": self.fc,
            "description": self.description,
            "is_custom": self.is_custom,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Material":
        """Create from dictionary."""
        return cls(
            id=UUID(data["id"]) if "id" in data else uuid4(),
            name=data["name"],
            material_type=MaterialType(data.get("material_type", "other")),
            standard=MaterialStandard(data.get("standard", "Custom")),
            E=float(data["E"]),
            nu=float(data["nu"]),
            rho=float(data["rho"]),
            fy=float(data["fy"]) if data.get("fy") is not None else None,
            fu=float(data["fu"]) if data.get("fu") is not None else None,
            fc=float(data["fc"]) if data.get("fc") is not None else None,
            description=data.get("description", ""),
            is_custom=data.get("is_custom", False),
        )

    def copy(self, new_name: str | None = None) -> "Material":
        """
        Create a copy of this material.

        Args:
            new_name: Optional new name for the copy

        Returns:
            New Material instance with same properties but new ID
        """
        return Material(
            id=uuid4(),
            name=new_name if new_name is not None else f"{self.name} (copy)",
            material_type=self.material_type,
            standard=MaterialStandard.CUSTOM,  # Copies become custom
            E=self.E,
            nu=self.nu,
            rho=self.rho,
            fy=self.fy,
            fu=self.fu,
            fc=self.fc,
            description=self.description,
            is_custom=True,
        )


# Unit conversion helpers (all internal units are kPa for stress, kg/m³ for density)
def mpa_to_kpa(mpa: float) -> float:
    """Convert MPa to kPa."""
    return mpa * 1000


def ksi_to_kpa(ksi: float) -> float:
    """Convert ksi to kPa."""
    return ksi * 6894.76
