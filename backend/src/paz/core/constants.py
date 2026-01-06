"""
Global constants for PAZ application.

These constants define application-wide limits and defaults.
"""

from typing import Final


# Application metadata
APP_NAME: Final[str] = "PAZ"
VERSION: Final[str] = "1.0.0a1"
DESCRIPTION: Final[str] = "Software Profesional de Análisis Estructural"

# MVP Limits (from PRD)
MAX_NODES: Final[int] = 50_000
MAX_ELEMENTS: Final[int] = 25_000
MAX_LOAD_CASES: Final[int] = 100
MAX_LOAD_COMBINATIONS: Final[int] = 500

# Undo/Redo
MAX_UNDO_LEVELS: Final[int] = 50

# Tolerances
NODE_DUPLICATE_TOLERANCE: Final[float] = 0.001  # meters
COORDINATE_PRECISION: Final[int] = 6  # decimal places
MIN_FRAME_LENGTH: Final[float] = 0.01  # meters

# Performance targets
TARGET_FPS_10K_ELEMENTS: Final[int] = 30
TARGET_ANALYSIS_TIME_10K: Final[int] = 30  # seconds
MAX_MEMORY_MB: Final[int] = 4096  # 4 GB

# Auto-save
AUTOSAVE_INTERVAL_SECONDS: Final[int] = 300  # 5 minutes
MAX_RECENT_PROJECTS: Final[int] = 10

# File format
PAZ_FILE_EXTENSION: Final[str] = ".paz"
PAZ_FILE_VERSION: Final[str] = "1.0"

# API
API_V1_PREFIX: Final[str] = "/api/v1"
DEFAULT_PAGE_SIZE: Final[int] = 50
MAX_PAGE_SIZE: Final[int] = 100

# Supported calculation engines
SUPPORTED_ENGINES: Final[tuple[str, ...]] = ("opensees", "kratos")
DEFAULT_ENGINE: Final[str] = "opensees"
