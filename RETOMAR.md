# RETOMAR.md

> Lee este archivo primero si eres una IA nueva retomando este proyecto.

---

## PROYECTO
**Nombre**: PAZ (Strux)
**Estado**: en progreso
**Última actividad**: 2026-01-06 22:15

---

## LEER PRIMERO

1. `feature_list.json` - Lista de features con estado (passes: true/false)
2. `CLAUDE.md` - Instrucciones del proyecto
3. `Documentación/ARQUITECTURA.md` - Stack técnico y estructura

---

## ESTADO ACTUAL

**Modo**: automático (feature_list.json)
**Progreso**: 5/18 features completadas

| Feature | Nombre | Estado |
|---------|--------|--------|
| F00 | Setup del Proyecto | ✅ `passes: true` |
| F31 | Gestión de Proyectos | ✅ `passes: true` |
| F01 | Modelación de Nodos | ✅ `passes: true` |
| F08 | Librería de Materiales | ✅ `passes: true` |
| F09 | Librería de Secciones AISC | ✅ `passes: true` |
| F12 | Perfiles Parametrizados | ❌ pendiente |
| ... | (12 features más) | ❌ pendiente |

### Última sesión (2026-01-06)
- Implementado F09: Section dataclass, SectionsRepository, 257 perfiles W AISC
- Script `scripts/generate_aisc_sections.py` para expandir perfiles (pendiente: HSS, L, C, Pipe, WT)
- 218 tests pasando, mypy strict, ruff clean

### Próxima tarea
**F12 - Perfiles Parametrizados** (ISection, RectangularHollow, CircularHollow, etc.)

---

## DECISIONES IMPORTANTES

| Decisión | Valor | Razón |
|----------|-------|-------|
| Arquitectura | Cloud-first (SaaS) | Sin instalación, suscripción |
| Motor de cálculo | OpenSees preferido | Especializado en estructuras |
| Backend | Python 3.12 + FastAPI | Compatible con openseespy |
| Frontend | React + Three.js | 3D en browser |
| Unidades internas | kPa, kg/m³, m | Consistencia SI |
| Perfiles AISC | 257 W shapes (parcial) | Ver scripts/generate_aisc_sections.py para expandir |

---

## ARCHIVOS MODIFICADOS RECIENTEMENTE

```
backend/src/paz/
├── core/           # constants, exceptions, units, logging
├── domain/
│   ├── model/      # project, node, restraint, structural_model
│   ├── materials/  # material.py
│   └── sections/   # section.py (NEW)
├── application/
│   ├── commands/   # node_commands, base_command
│   └── services/   # project_service, autosave_service, undo_redo_service
└── infrastructure/
    └── repositories/  # file_repository, materials_repository, sections_repository (NEW)

backend/src/data/
├── materials/
│   ├── steel_astm.json      # 9 aceros ASTM
│   ├── concrete_nch.json    # 6 hormigones NCh
│   └── concrete_eurocode.json  # 7 hormigones Eurocode
└── sections/
    └── aisc_w_shapes.json   # 257 perfiles W (NEW)

backend/scripts/
└── generate_aisc_sections.py  # Script para generar más perfiles AISC (NEW)

backend/tests/  # 218 tests
```

---

## CÓMO CONTINUAR

### Para seguir con F12 (Perfiles Parametrizados):
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v  # Verificar que todo pasa
```

Luego implementar:
1. `domain/sections/parametric.py` - Clases base parametricas
2. `domain/sections/i_section.py` - ISection(bf, tf, d, tw)
3. `domain/sections/rectangular_section.py` - RectangularHollow, RectangularSolid
4. `domain/sections/circular_section.py` - CircularHollow, CircularSolid
5. Tests unitarios

### Verificaciones obligatorias:
```bash
mypy src/paz --strict
ruff check src/paz
pytest tests/ -v
```

---

## REPOSITORIO

- **GitHub**: https://github.com/kcortes765/strux
- **Branch**: main

---

*Generado: 2026-01-06 22:15*
