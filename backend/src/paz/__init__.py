"""
PAZ - Software Profesional de Análisis Estructural

Un software cloud-first para análisis estructural que combina:
- Potencia de cálculo (OpenSees + motores intercambiables)
- Visualización 3D web (Three.js)
- Backend moderno (FastAPI + Python 3.11/3.12)
- Normativas: NCh (Chile), AISC, Eurocódigos
"""

__version__ = "1.0.0a1"
__author__ = "Pablo & Kevin"

from paz.core.constants import APP_NAME, VERSION


__all__ = ["APP_NAME", "VERSION", "__version__"]
