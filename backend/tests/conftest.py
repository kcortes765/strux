"""
Pytest configuration and shared fixtures for PAZ tests.
"""

import pytest
from typing import Generator, Any
from httpx import AsyncClient, ASGITransport

from paz.app import create_app


@pytest.fixture(scope="session")
def app():
    """Create application instance for testing."""
    return create_app()


@pytest.fixture
async def client(app) -> Generator[AsyncClient, None, None]:
    """Create async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_node_data() -> dict[str, Any]:
    """Sample node data for testing."""
    return {
        "id": 1,
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "restraint": {
            "ux": True,
            "uy": True,
            "uz": True,
            "rx": True,
            "ry": True,
            "rz": True,
        },
    }


@pytest.fixture
def sample_frame_data() -> dict[str, Any]:
    """Sample frame data for testing."""
    return {
        "id": 1,
        "node_i_id": 1,
        "node_j_id": 2,
        "material_id": "A36",
        "section_id": "W12x26",
        "rotation": 0.0,
    }


@pytest.fixture
def sample_material_data() -> dict[str, Any]:
    """Sample material data for testing (ASTM A36 Steel)."""
    return {
        "id": "A36",
        "name": "ASTM A36 Steel",
        "type": "steel",
        "E": 200e9,  # Pa
        "G": 77e9,  # Pa
        "nu": 0.3,
        "rho": 7850,  # kg/m³
        "fy": 250e6,  # Pa
        "fu": 400e6,  # Pa
    }


@pytest.fixture
def sample_section_data() -> dict[str, Any]:
    """Sample section data for testing (W12x26)."""
    return {
        "id": "W12x26",
        "name": "W12x26",
        "type": "W",
        "A": 0.00494,  # m²
        "Ix": 8.49e-5,  # m⁴
        "Iy": 1.70e-5,  # m⁴
        "Iz": 1.70e-5,  # m⁴
        "Sx": 0.000571,  # m³
        "Sy": 0.000138,  # m³
        "rx": 0.131,  # m
        "ry": 0.0587,  # m
    }


@pytest.fixture
def sample_project_data() -> dict[str, Any]:
    """Sample project data for testing."""
    return {
        "name": "Test Project",
        "units": {
            "length": "m",
            "force": "kN",
            "angle": "deg",
        },
    }
