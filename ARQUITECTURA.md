# Arquitectura Tecnica - PAZ

**Software Profesional de Analisis Estructural**

Documento: Arquitectura v1.1 (Consolidado)
Fecha: 2026-01-03
Fase: 6.0 - Consolidacion Final

---

## 1. Resumen Ejecutivo

### 1.1 Vision Arquitectonica

PAZ adopta una arquitectura modular en capas que permite:
- Intercambio de motores de calculo (OpenSees MVP, Kratos produccion)
- Evolucion independiente de UI, logica de negocio y persistencia
- Extensibilidad para nuevos tipos de elementos y normativas
- Portabilidad futura a otras plataformas

### 1.2 Principios Arquitectonicos

| Principio | Descripcion | Aplicacion |
|-----------|-------------|------------|
| **Separacion de Concerns** | Cada capa tiene responsabilidad unica | UI, Domain, Infrastructure separadas |
| **Dependency Inversion** | Depender de abstracciones, no implementaciones | Interfaces para motores de calculo |
| **Single Source of Truth** | Un unico lugar para cada dato | Modelo centralizado en Domain |
| **Fail Fast** | Detectar errores temprano | Validacion en boundaries |
| **Convention over Configuration** | Defaults sensatos | Configuracion minima para empezar |

---

## 2. Stack Tecnologico

### 2.1 Decisiones de Stack

| Capa | Tecnologia | Version | Justificacion |
|------|------------|---------|---------------|
| **Lenguaje Backend** | Python | 3.11/3.12 | Alineado con openseespy y acelerado, evitan conflictos de version con los engines |
| **Framework API** | FastAPI | 0.100+ | Alto rendimiento, async, tipado |
| **Frontend** | React | 18+ | Ecosistema maduro, componentes |
| **Visualizacion 3D** | Three.js | latest | 3D en browser, WebGL |
| **Motor Calculo** | OpenSees + adaptador multi-motor | 3.x | OpenSees esta especializado en estructuras, con adaptadores para Kratos/RISA cuando se requiera |
| **Base de Datos** | PostgreSQL | 15+ | Cloud-ready, robusto |
| **Auth** | Clerk/Auth0 | - | Rapido de implementar |
| **Pagos** | Stripe | - | Suscripciones automaticas |
| **Hosting** | Railway/Render | - | Simple, escalable |
| **Testing** | pytest + hypothesis | - | Testing propiedades + fixtures |

### 2.2 Justificacion Detallada

#### 2.2.1 Cloud-First vs Desktop

| Criterio | Cloud (SaaS) | Desktop |
|----------|--------------|---------|
| Instalacion | Ninguna | Compleja |
| Pirateria | Imposible | Facil |
| Updates | Automaticos | Manuales |
| Cobro recurrente | Natural | Dificil |
| Multiplataforma | Automatico | Builds separados |
| **Decision** | **SELECCIONADO** | Descartado |

**Razon**: Cloud simplifica distribucion, elimina pirateria, y facilita modelo de suscripcion.

#### 2.2.2 OpenSees preferido y motores intercambiables

| Criterio | OpenSees | Adaptadores (Kratos, RISA) |
|----------|----------|--------------------------|
| Licencia | Open Source | BSD (Kratos) |
| Enfoque | Especializado en estructuras | Amplia coverage (Kratos/RISA) |
| Python API | openseespy (3.11/3.12) | Kratos API / RISA OAPI |
| Performance | Alto para frames y shells | Complementario para ciertos casos |
| Analisis soportados | Estatico, Dinamico, No lineal, Tiempo-historia | Usable cuando el usuario lo requiere |
| **Decision** | **PRIORITARIO** | **RESERVADO** |

**Razon**: OpenSees entrega enfoque estructural y versionado compatible; los adaptadores permiten cambiar a Kratos o RISA cuando sea necesario sin reescribir la logica de dominio.

---

## 3. Arquitectura de Alto Nivel

### 3.1 Diagrama de Capas (Cloud)

```
+------------------------------------------------------------------+
|                     FRONTEND (React + Three.js)                   |
|  +------------------+  +------------------+  +-----------------+  |
|  |    App Shell     |  |  ViewportCanvas  |  |  PropertyPanel  |  |
|  |    (React)       |  |   (Three.js)     |  |   (React)       |  |
|  +------------------+  +------------------+  +-----------------+  |
------------------------------------------------------------------+
                                | HTTPS/WebSocket
                                 v
+------------------------------------------------------------------+
|                     BACKEND (FastAPI + Python)                    |
|  +------------------+  +------------------+  +-----------------+  |
|  | ProjectRouter    |  | AnalysisRouter   |  | ExportRouter    |  |
|  +------------------+  +------------------+  +-----------------+  |
|  +------------------+  +------------------+  +-----------------+  |
|  | AuthMiddleware   |  | BillingService   |  | WebSocketMgr    |  |
|  +------------------+  +------------------+  +-----------------+  |
+------------------------------------------------------------------+
                                |
                                 v
------------------------------------------------------------------+
|                         DOMAIN LAYER                              |
|  +------------------+  +------------------+  +------------------+  |
|  |   StructuralModel|  |   GridManager    |  | SectionDesigner |  |
|  |   (Nodes,Frames) |  | (Grillas, Snap)  |  | (Secciones)     |  |
|  +------------------+  +------------------+  +------------------+  |
|  +------------------+  +------------------+  +------------------+  |
|  |    Materials     |  |    Sections     |  | UnitConversionSvc|  |
|  |    Library       |  |    Library      |  |                 |  |
|  +------------------+  +------------------+  +------------------+  |
|  +------------------+  +------------------+  +-----------------+  |
|  |   LoadCases      |  |  LoadCombinations|  |    Results      |  |
|  +------------------+  +------------------+  +-----------------+  |
+------------------------------------------------------------------+
                                |
                                 v
+------------------------------------------------------------------+
|                     INFRASTRUCTURE LAYER                          |
|  +------------------+  +------------------+  +-----------------+  |
|  | OpenSeesAdapter  |  |  PostgreSQL      |  | StripeService   |  |
|  | (multi-motor)    |  |  (proyectos)     |  | (pagos)         |  |
|  +------------------+  +------------------+  +-----------------+  |
|  +------------------+  +------------------+  +-----------------+  |
|  | AutoCADImporter  |  |  MaterialsRepo   |  | SectionsRepo    |  |
|  | (lineas -> nodos)|  |  (JSON files)    |  | (JSON files)    |  |
|  +------------------+  +------------------+  +-----------------+  |
|  +------------------+  +------------------+  +-----------------+  |
|  | UnitConversionSvc|  | S3/Storage       |  |  KratosAdapter  |  |
|  |                  |  |  (archivos)      |  |  (fallback)     |  |
|  +------------------+  +------------------+  +-----------------+  |
+------------------------------------------------------------------+
```

### 3.2 Flujo de Datos Principal

```
Browser -> React App -> API Call -> FastAPI -> Domain Model -> PostgreSQL
                                       |
                                       v
                         OpenSeesAdapter -> OpenSees Engine (Kratos/RISA optional)
                                       |
                                       v
                                  Results -> WebSocket -> React -> Three.js Update
```

### 3.3 Componentes Principales

| Componente | Responsabilidad | Dependencias |
|------------|-----------------|--------------|
| **React App** | UI shell, routing, state | Three.js, API client |
| **ViewportCanvas** | Render 3D, picking, orbit | Three.js, Domain Model |
| **FastAPI Backend** | API REST, WebSocket, auth | Domain, OpenSeesAdapter |
| **ProjectRouter** | CRUD proyectos | PostgreSQL |
| **AnalysisRouter** | Orquestar analisis | OpenSeesAdapter |
| **StructuralModel** | Nodos, elementos, cargas | Materials, Sections, GridManager |
| **GridManager** | Grilla y snapping | StructuralModel, ViewportCanvas |
| **SectionDesigner** | Editor de secciones mixtas | StructuralModel, Sections |
| **UnitConversionService** | Conversion de unidades | core/units, UI |
| **OpenSeesAdapter** | Interfaz con OpenSees y adaptadores | OpenSees, Domain Model |
| **KratosAdapter** | Interfaz de respaldo con Kratos | Kratos Multiphysics |
| **AutoCADImporter** | Convertir lineas a nodos/frames | DXF, UnitConversionService |
| **StripeService** | Suscripciones, pagos | Stripe API |

El dominio incorpora `GridManager` y `SectionDesigner` para mantener el enfoque en el analisis: las grillas guian la modelacion y el diseñador de secciones genera perfiles mixtos que se guardan en la libreria. `UnitConversionService` alimenta UI y cargar/responder conversiones antes de enviarlas al motor. `AutoCADImporter` en la capa de infraestructura convierte lineas en nodos/frames y respeta las unidades del proyecto.

El adapter principal es `OpenSeesAdapter`, con `KratosAdapter` como fallback para benchmarks, y tanto `GridManager` como el conversor de unidades se exponen al frontend sin habilitar funciones de diseno legalmente sensibles. La arquitectura tambien considera pipelines de empaquetado macOS y pruebas de Safari/WebGL para la segunda fase.

---

## 4. Estructura de Carpetas

```
paz/
|-- backend/                         # FastAPI Backend
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py                  # FastAPI app
|   |   |-- config.py                # Settings
|   |   |
|   |   |-- routers/                 # API Endpoints
|   |   |   |-- projects.py
|   |   |   |-- analysis.py
|   |   |   |-- materials.py
|   |   |   |-- sections.py
|   |   |   |-- export.py
|   |   |
|   |   |-- services/                # Business Logic
|   |   |   |-- project_service.py
|   |   |   |-- analysis_service.py
|   |   |   |-- billing_service.py
|   |   |
|   |   |-- domain/                  # Domain Models
|   |   |   |-- structural_model.py
|   |   |   |-- node.py
|   |   |   |-- frame.py
|   |   |   |-- material.py
|   |   |   |-- section.py
|   |   |   |-- section_designer.py  # Secciones mixtas/custom
|   |   |   |-- grid_manager.py      # Sistema de grillas
|   |   |   |-- loads.py
|   |   |   |-- results.py
|   |   |
|   |   |-- infrastructure/          # External Services
|   |   |   |-- opensees_adapter.py  # Motor preferido
|   |   |   |-- kratos_adapter.py    # Motor alternativo
|   |   |   |-- autocad_importer.py  # Importador DXF
|   |   |   |-- database.py          # PostgreSQL
|   |   |   |-- storage.py           # S3/files
|   |   |   |-- stripe_client.py     # Pagos
|   |   |
|   |   |-- core/                    # Utilities
|   |       |-- units.py             # Conversion kN<->ton, m<->ft, etc.
|   |       |-- constants.py
|   |       |-- exceptions.py
|   |
|   |-- data/                        # Datos estaticos
|   |   |-- materials/
|   |   |-- sections/
|   |
|   |-- tests/
|   |-- pyproject.toml
|
|-- frontend/                        # React Frontend
|   |-- src/
|   |   |-- components/
|   |   |   |-- Viewport.tsx         # Three.js canvas
|   |   |   |-- GridOverlay.tsx      # Visualizacion de grillas
|   |   |   |-- SectionDesigner.tsx  # Editor de secciones
|   |   |   |-- UnitConverter.tsx    # Conversor rapido
|   |   |   |-- PropertyPanel.tsx
|   |   |   |-- ModelTree.tsx
|   |   |   |-- Toolbar.tsx
|   |   |
|   |   |-- hooks/
|   |   |   |-- useProject.ts
|   |   |   |-- useAnalysis.ts
|   |   |
|   |   |-- api/
|   |   |   |-- client.ts
|   |   |
|   |   |-- App.tsx
|   |   |-- main.tsx
|   |
|   |-- package.json
|
|-- docker-compose.yml
|-- README.md
```

### 4.1 Convenciones de Nomenclatura

| Elemento | Convencion | Ejemplo |
|----------|------------|---------|
| Modulos | snake_case | `structural_model.py` |
| Clases | PascalCase | `StructuralModel` |
| Funciones | snake_case | `create_node()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_NODES` |
| Privados | _prefijo | `_internal_method()` |
| Interfaces | I prefijo | `IEngineAdapter` |
| DTOs | Sufijo DTO | `NodeDTO` |
| Exceptions | Sufijo Error | `ValidationError` |

### 4.2 Terminologia Estandarizada

| En Codigo | En Documentacion ES | Notas |
|-----------|---------------------|-------|
| Section | Seccion | Propiedades geometricas/mecanicas |
| Engine | Motor de Calculo | Solver (OpenSees, Kratos) |
| Frame | Frame | Elemento lineal |
| Shell | Shell | Elemento de superficie |

---

## 5. Modelo de Datos

### 5.1 Diagrama de Entidades

```
+------------------+       +------------------+
|   Project        |       |  StructuralModel |
+------------------+       +------------------+
| id: UUID         |1     1| id: UUID         |
| name: str        |------>| nodes: List[Node]|
| units: UnitSystem|       | frames: List[Fr] |
| created_at: dt   |       | materials: dict  |
| modified_at: dt  |       | sections: dict   |
+------------------+       +------------------+
                                   |
           +-----------------------+-----------------------+
           |                       |                       |
           v                       v                       v
   +-------------+         +-------------+         +-------------+
   |    Node     |         |    Frame    |         |   LoadCase  |
   +-------------+         +-------------+         +-------------+
   | id: int     |         | id: int     |         | id: int     |
   | x: float    |         | node_i: int |         | name: str   |
   | y: float    |         | node_j: int |         | type: enum  |
   | z: float    |         | material_id |         | loads: List |
   | restraint   |         | section_id  |         +-------------+
   +-------------+         | releases    |
                           | rotation    |
                           +-------------+
                                   |
           +-----------------------+-----------------------+
           |                       |
           v                       v
   +-------------+         +------------------+
   |  Material   |         |    Section       |
   +-------------+         +------------------+
   | id: str     |         | id: str          |
   | name: str   |         | name: str        |
   | type: enum  |         | type: enum       |
   | E: float    |         | A: float         |
   | G: float    |         | Ix, Iy, Iz: float|
   | nu: float   |         | Sx, Sy: float    |
   | rho: float  |         | rx, ry: float    |
   | fy: float   |         | shape_data: dict |
   +-------------+         +------------------+
```

### 5.2 Formato de Archivo .paz

```json
{
  "version": "1.0",
  "project": {
    "id": "uuid",
    "name": "Edificio Example",
    "units": {
      "length": "m",
      "force": "kN",
      "angle": "deg"
    },
    "created_at": "2026-01-03T10:00:00Z",
    "modified_at": "2026-01-03T15:30:00Z"
  },
  "model": {
    "nodes": [
      {"id": 1, "x": 0.0, "y": 0.0, "z": 0.0, "restraint": [1,1,1,1,1,1]}
    ],
    "frames": [
      {"id": 1, "node_i": 1, "node_j": 3, "material": "A36", "section": "W12x26"}
    ],
    "materials": {
      "A36": {"type": "steel", "E": 200e9, "fy": 250e6}
    },
    "sections": {
      "W12x26": {"type": "W", "A": 0.00494, "Ix": 8.49e-5}
    }
  },
  "load_cases": [],
  "load_combinations": [],
  "results": {}
}
```

**Nota**: El archivo .paz es JSON comprimido con gzip. Es el formato nativo del proyecto, no un formato de intercambio.

---

## 6. APIs e Integraciones

### 6.1 Interfaz del Motor de Calculo (Multi-Engine)

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.structural_model import StructuralModel
from app.domain.results import AnalysisResults

class IEngineAdapter(ABC):
    """Interfaz abstracta para motores de calculo intercambiables"""

    @abstractmethod
    def validate_model(self, model: StructuralModel) -> List[str]:
        """Valida el modelo y retorna lista de errores"""
        pass

    @abstractmethod
    async def run_static_analysis(
        self,
        model: StructuralModel,
        load_cases: List[str],
        progress_callback: Optional[callable] = None
    ) -> AnalysisResults:
        """Ejecuta analisis estatico lineal"""
        pass

class OpenSeesAdapter(IEngineAdapter):
    """Adapter principal para OpenSees - motor preferido"""

    def get_engine_info(self) -> dict:
        return {"name": "OpenSees", "version": "3.x", "license": "BSD"}

class KratosAdapter(IEngineAdapter):
    """Adapter alternativo para Kratos Multiphysics"""

    def get_engine_info(self) -> dict:
        return {"name": "Kratos Multiphysics", "version": "10.x", "license": "BSD"}
```

### 6.2 Event Bus

```python
from enum import Enum, auto

class EventType(Enum):
    MODEL_CHANGED = auto()
    NODE_CREATED = auto()
    NODE_DELETED = auto()
    FRAME_CREATED = auto()
    FRAME_DELETED = auto()
    SELECTION_CHANGED = auto()
    ANALYSIS_STARTED = auto()
    ANALYSIS_COMPLETED = auto()
    ANALYSIS_FAILED = auto()
    PROJECT_SAVED = auto()
    PROJECT_LOADED = auto()
```

### 6.3 Sistema de Comandos (Undo/Redo)

```python
from abc import ABC, abstractmethod

class Command(ABC):
    """Comando base para operaciones reversibles"""

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass
```

---

## 7. Patrones de Diseno

| Patron | Uso en PAZ | Ejemplo |
|--------|------------|---------|
| **Adapter** | Motores de calculo intercambiables | `OpenSeesAdapter`, `KratosAdapter` |
| **Repository** | Acceso a datos | `MaterialsRepository`, `SectionsRepository` |
| **Service** | Logica de negocio | `AnalysisService`, `ProjectService`, `UnitConversionService` |
| **DTO** | Transferencia de datos | `NodeDTO`, `FrameDTO` |
| **Factory** | Creacion de objetos | `SectionFactory`, `SectionDesigner` |
| **Strategy** | Algoritmos intercambiables | Diferentes motores de analisis |

---

## 8. Rendimiento y Escalabilidad

### 8.1 Rendimiento por Tamano de Modelo

| Tamano | Nodos | Elementos | Target Render | Target Analisis |
|--------|-------|-----------|---------------|-----------------|
| Pequeno | < 1,000 | < 500 | > 60 FPS | < 5s |
| Mediano | < 10,000 | < 5,000 | > 30 FPS | < 30s |
| Grande | < 50,000 | < 25,000 | > 15 FPS | < 2min |
| Muy grande | < 100,000 | < 50,000 | > 10 FPS | < 5min |

### 8.2 Estrategias de Optimizacion

- **LOD (Level of Detail)**: Reducir detalle segun zoom
- **Instancing**: Reutilizar geometria para secciones repetidas
- **Culling**: No renderizar elementos fuera de vista
- **Caching**: Cache de meshes por seccion

---

## 9. Deployment

### 9.1 Build Pipeline (CI/CD)

```
Source Code -> Type Check (mypy) -> Lint (ruff) -> Tests (pytest)
           -> Build Docker -> Push to Registry -> Deploy to Railway/Render
```

### 9.2 Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - STRIPE_SECRET_KEY=...
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### 9.3 Estructura de Deploy

```
Cloud (Railway/Render)
|-- Backend Service (FastAPI + OpenSeesAdapter)
|-- Frontend Service (React static)
|-- PostgreSQL Database
|-- Redis (cache, opcional)
|-- macOS packaging pipeline (Nuitka/PyInstaller) para builds nativos
```

---

## 10. Referencias

### 10.1 Documentacion Externa

| Recurso | URL | Proposito |
|---------|-----|-----------|
| FastAPI | https://fastapi.tiangolo.com/ | Backend API |
| React | https://react.dev/ | Frontend |
| Three.js | https://threejs.org/ | Visualizacion 3D |
| OpenSees | https://opensees.berkeley.edu/ | Motor calculo preferido |
| Kratos | https://github.com/KratosMultiphysics/Kratos | Motor calculo alternativo |
| Stripe | https://stripe.com/docs | Pagos |
| AISC | https://www.aisc.org/ | Perfiles acero |
| Eurocode | https://eurocodes.jrc.ec.europa.eu/ | Normativa europea |

### 10.2 Documentos Internos

- `BRIEF.md` - Brief del proyecto
- `PRD.md` - Product Requirements Document
- `feature_list.json` - Lista de features ejecutable

---

*Arquitectura consolidada - Fase 6.0 DocGen*
*Proyecto PAZ - Software Profesional de Analisis Estructural*
