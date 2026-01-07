"""
Custom exceptions for PAZ application.

All custom exceptions inherit from PazError for consistent error handling.
"""

from typing import Any


class PazError(Exception):
    """Base exception for all PAZ errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ValidationError(PazError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str | None = None, **kwargs: Any) -> None:
        details = {"field": field, **kwargs} if field else kwargs
        super().__init__(message, details)


class ModelError(PazError):
    """Raised when structural model operations fail."""

    pass


class NodeError(ModelError):
    """Raised when node operations fail."""

    def __init__(self, message: str, node_id: int | None = None, **kwargs: Any) -> None:
        details = {"node_id": node_id, **kwargs} if node_id else kwargs
        super().__init__(message, details)


class FrameError(ModelError):
    """Raised when frame operations fail."""

    def __init__(
        self, message: str, frame_id: int | None = None, **kwargs: Any
    ) -> None:
        details = {"frame_id": frame_id, **kwargs} if frame_id else kwargs
        super().__init__(message, details)


class DuplicateNodeError(NodeError):
    """Raised when attempting to create a duplicate node."""

    def __init__(
        self, x: float, y: float, z: float, existing_node_id: int | None = None
    ) -> None:
        message = f"Node already exists at coordinates ({x}, {y}, {z})"
        super().__init__(
            message,
            node_id=existing_node_id,
            coordinates={"x": x, "y": y, "z": z},
        )


class AnalysisError(PazError):
    """Raised when analysis operations fail."""

    pass


class UnstableModelError(AnalysisError):
    """Raised when the structural model is unstable."""

    def __init__(self, message: str = "Model is unstable", **kwargs: Any) -> None:
        super().__init__(message, kwargs)


class EngineError(AnalysisError):
    """Raised when calculation engine operations fail."""

    def __init__(
        self, message: str, engine: str | None = None, **kwargs: Any
    ) -> None:
        details = {"engine": engine, **kwargs} if engine else kwargs
        super().__init__(message, details)


class FileError(PazError):
    """Raised when file operations fail."""

    def __init__(
        self, message: str, path: str | None = None, **kwargs: Any
    ) -> None:
        details = {"path": path, **kwargs} if path else kwargs
        super().__init__(message, details)


class ProjectNotFoundError(FileError):
    """Raised when a project file cannot be found."""

    def __init__(self, path: str) -> None:
        super().__init__(f"Project not found: {path}", path=path)


class InvalidProjectFileError(FileError):
    """Raised when a project file is invalid or corrupted."""

    def __init__(self, path: str, reason: str | None = None) -> None:
        message = f"Invalid project file: {path}"
        if reason:
            message += f" ({reason})"
        super().__init__(message, path=path, reason=reason)


class MaterialError(PazError):
    """Raised when material operations fail."""

    def __init__(
        self, message: str, material_id: str | None = None, **kwargs: Any
    ) -> None:
        details = {"material_id": material_id, **kwargs} if material_id else kwargs
        super().__init__(message, details)


class MaterialNotFoundError(MaterialError):
    """Raised when a material cannot be found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Material not found: {name}", material_id=name)


class SectionError(PazError):
    """Raised when section operations fail."""

    def __init__(
        self, message: str, section_id: str | None = None, **kwargs: Any
    ) -> None:
        details = {"section_id": section_id, **kwargs} if section_id else kwargs
        super().__init__(message, details)


class SectionNotFoundError(SectionError):
    """Raised when a section cannot be found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Section not found: {name}", section_id=name)


class UnitConversionError(PazError):
    """Raised when unit conversion fails."""

    def __init__(
        self,
        message: str,
        from_unit: str | None = None,
        to_unit: str | None = None,
        **kwargs: Any,
    ) -> None:
        details = {
            "from_unit": from_unit,
            "to_unit": to_unit,
            **kwargs,
        }
        super().__init__(message, details)
