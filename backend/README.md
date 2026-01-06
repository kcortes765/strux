# PAZ Backend

Software Profesional de Análisis Estructural - Backend API

## Stack

- Python 3.11/3.12
- FastAPI
- OpenSees (openseespy)
- PostgreSQL

## Desarrollo

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -e ".[dev]"

# Ejecutar servidor
uvicorn paz.app:app --reload

# Ejecutar tests
pytest

# Type checking
mypy src/paz --strict

# Linting
ruff check src/paz
```

## Estructura

```
backend/
├── src/paz/
│   ├── core/           # Utilidades, constantes, excepciones
│   ├── domain/         # Modelos de dominio (Node, Frame, etc.)
│   ├── application/    # Servicios y comandos
│   └── infrastructure/ # Adaptadores externos (OpenSees, DB)
├── tests/
└── data/               # Materiales y secciones predefinidos
```
