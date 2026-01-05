# CLAUDE.md - PAZ

## Sistema: PAZ v1.0-MVP

**Software Profesional de Analisis Estructural**

---

## Proposito

PAZ (nombre en evaluacion: Nifes Forge / Structural Forge) es un software de analisis estructural cloud para ingenieros civiles. Combina:
- Potencia de calculo (OpenSees preferido + motores intercambiables)
- Visualizacion 3D web (Three.js)
- Backend moderno (FastAPI + Python 3.11/3.12)
- Frontend React con Grillas, Section Designer, Conversor de unidades
- Normativas: NCh (Chile), AISC, Eurocodigos
- Precio accesible ($30-50/mes)

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|------------|
| Backend | Python 3.11/3.12 + FastAPI |
| Frontend | React 18+ / TypeScript |
| Visualizacion 3D | Three.js |
| Motor Calculo | OpenSees (preferido) + Kratos (alternativo) |
| Base de Datos | PostgreSQL |
| Auth | Clerk / Auth0 |
| Pagos | Stripe |
| Hosting | Railway / Render |
| Testing | pytest, hypothesis |
| macOS | Soporte futuro (V1.0) |

---

## Estructura del Proyecto

```
paz/
|-- backend/              # FastAPI + OpenSees/Kratos
|   |-- app/
|   |   |-- routers/      # API endpoints
|   |   |-- services/     # Business logic
|   |   |-- domain/       # Modelo, GridManager, SectionDesigner
|   |   |-- infrastructure/  # OpenSees, Kratos, AutoCAD, DB
|   |   |-- core/         # units.py (kN<->ton, m<->ft)
|   |-- data/             # Materiales, secciones AISC/NCh/Euro
|   |-- tests/
|
|-- frontend/             # React + Three.js
|   |-- src/
|   |   |-- components/   # Viewport, GridOverlay, SectionDesigner, UnitConverter
|   |   |-- hooks/        # useProject, useAnalysis
|   |   |-- api/          # API client
```

---

## Comandos Frecuentes

```bash
# Backend
cd backend
pip install -e .
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Tests
pytest backend/tests

# Deploy
docker-compose up --build
```

---

## Arquitectura

### Capas
1. **Frontend**: React App, ViewportCanvas (Three.js), GridOverlay, SectionDesigner, UnitConverter
2. **API**: FastAPI routers, WebSocket para resultados
3. **Services**: ProjectService, AnalysisService, BillingService, UnitConversionService
4. **Domain**: StructuralModel, Node, Frame, Material, Section, GridManager, SectionDesigner, Results
5. **Infrastructure**: OpenSeesAdapter (preferido), KratosAdapter (alternativo), AutoCADImporter, PostgreSQL, Stripe

### Patrones
- **Adapter**: OpenSeesAdapter, KratosAdapter (motores intercambiables)
- **Repository**: Acceso a datos (materiales, secciones)
- **Service**: Logica de negocio
- **Factory**: SectionDesigner para secciones custom/mixtas

---

## Features MVP (18 features)

| ID | Feature | Estado |
|----|---------|--------|
| F00 | Setup Proyecto | Pendiente |
| F31 | Gestion Proyectos | Pendiente |
| F01 | Nodos | Pendiente |
| F35 | Sistema de Grillas | Pendiente |
| F36 | Section Designer | Pendiente |
| F37 | Conversor de Unidades | Pendiente |
| F08 | Materiales | Pendiente |
| F09 | Secciones AISC | Pendiente |
| F12 | Perfiles Parametrizados | Pendiente |
| F02 | Frames | Pendiente |
| F13 | Analisis Estatico (OpenSees) | Pendiente |
| F18 | Visualizacion Desplazamientos | Pendiente |
| F19 | Visualizacion Esfuerzos | Pendiente |
| F21 | Perfiles Extruidos | Pendiente |
| F33 | Export/Import (incl. AutoCAD) | Pendiente |
| F-UI | Interfaz Usuario | Pendiente |
| F-FINAL | Integracion | Pendiente |
| F38 | Compatibilidad macOS | Post-MVP |

---

## Documentacion

| Documento | Ubicacion |
|-----------|-----------|
| Brief | `docs/BRIEF.md` |
| PRD | `docs/PRD.md` |
| Arquitectura | `docs/ARQUITECTURA.md` |
| Feature List | `feature_list.json` |

---

## Convenciones

### Codigo
- **Modulos**: snake_case (`structural_model.py`)
- **Clases**: PascalCase (`StructuralModel`)
- **Funciones**: snake_case (`create_node()`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_NODES`)
- **Interfaces**: I prefijo (`IEngineAdapter`)

### Terminologia
| En Codigo | En UI/Docs ES |
|-----------|---------------|
| Section | Seccion |
| Engine | Motor de Calculo |
| Frame | Frame |
| Shell | Shell |

---

## Limites MVP

| Recurso | Limite |
|---------|--------|
| Nodos | 50,000 |
| Tiempo analisis 10k elem | < 30s |
| FPS render 10k elem | > 30 |
| Memoria max | 4 GB |
| Undo/Redo niveles | 50 |

---

## Notas Importantes

1. **OpenSees es el motor preferido** - Con adaptadores para Kratos cuando el usuario lo requiera.

2. **Cloud-first** - Web (React + FastAPI). macOS en V1.0.

3. **Validacion vs SAP2000/Robot/RISA** - Benchmarking automatizado para credibilidad.

4. **Normativas**: NCh (Chile), AISC (general), Eurocodigos. Sin NSR Colombia por ahora.

5. **Python 3.11/3.12** - Versiones compatibles con openseespy. Evitar conflictos.

6. **Nombre pendiente** - "PAZ", "Nifes Forge", o "Structural Forge" en evaluacion.

7. **Enfoque en Analisis** - El Diseno estructural queda para fases futuras (complejidad legal).

---

## Contacto

- Ingeniero Estructural: Pablo
- Product Manager: Kevin

---

*Generado por DocGen - Fase 6.0*
