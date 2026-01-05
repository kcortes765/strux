# Resumen Ejecutivo - Strux

**Software Profesional de Analisis Estructural (Cloud)**

Fecha: 2026-01-04
Version: 1.0-MVP
Nombre: Strux (en evaluacion: Nifes Forge / Structural Forge)

---

## Vision

Strux sera el software de analisis estructural de referencia: una herramienta profesional, moderna y economicamente accesible que democratiza el acceso a tecnologia de ingenieria de clase mundial, con enfoque en analisis (no diseno) y normativas NCh, AISC y Eurocodigos.

---

## Propuesta de Valor

| Problema | Solucion Strux |
|----------|----------------|
| Licencias prohibitivas ($4,000-$17,000 USD/ano) | $30-50 USD/mes (cloud) |
| Sin soporte para normativas regionales | NCh (Chile), AISC, Eurocodigos integrados |
| Interfaces anticuadas, curva de aprendizaje alta | UX moderna, grillas inteligentes, Section Designer |
| Interoperabilidad limitada | Importador AutoCAD, conversor de unidades estilo Mathcad |
| Dependencia de un solo motor | OpenSees preferido + Kratos alternativo (usuario elige) |

---

## Diferenciadores vs Competencia

| Competidor | Debilidad | Ventaja Strux |
|------------|-----------|---------------|
| SAP2000 | $17,000+, curva alta | 1/100 del precio, UX moderna |
| Robot | Bugs, solo Eurocodes | Estabilidad, multi-normativa |
| RISA | Dinamico poco confiable, solo USA | Analisis robusto, NCh/Euro |
| SkyCiv | Sin no-lineal, limitado | Analisis avanzados, cloud |
| CYPECAD | Sin pushover/time-history | Analisis avanzados |

---

## Stack Tecnologico (Cloud-First)

| Componente | Tecnologia |
|------------|------------|
| Backend | Python 3.11/3.12 + FastAPI |
| Frontend | React 18+ / TypeScript |
| Visualizacion 3D | Three.js |
| Motor Preferido | OpenSees |
| Motor Alternativo | Kratos Multiphysics |
| Base de Datos | PostgreSQL |
| Pagos | Stripe |
| Hosting | Railway / Render |

---

## Fases del Proyecto

### MVP (Meses 1-2)
- Arquitectura cloud (FastAPI + React + Three.js)
- Motor OpenSees con adaptadores multi-engine
- Modelacion: Nodos, Frames, Grillas, Section Designer
- Librerias: AISC, NCh, Eurocode
- Analisis: Estatico lineal (validado vs SAP2000/Robot/RISA)
- Visualizacion: Desplazamientos, esfuerzos, grillas overlay
- Importador AutoCAD, conversor de unidades
- Auth + Pagos (Stripe)
- Deploy cloud

### V1.0 (Meses 3-6)
- Shells, Releases, Grupos
- Analisis dinamico, Modos de vibrar
- Combinaciones normativas
- macOS (beta)
- App movil basica

### V2.0 (Meses 7-12)
- Membranas, Cables, Links
- Tiempo-historia, No lineal
- Verificaciones normativas completas
- Sincronizacion desktop-movil
- Plan Enterprise

---

## Features MVP (18 features)

| ID | Feature | Prioridad |
|----|---------|-----------|
| F00 | Setup Proyecto | Critica |
| F31 | Gestion Proyectos | Critica |
| F01 | Nodos | Critica |
| F35 | Sistema de Grillas | Critica |
| F36 | Section Designer | Critica |
| F37 | Conversor de Unidades | Alta |
| F08 | Materiales | Critica |
| F09 | Secciones AISC | Critica |
| F12 | Perfiles Parametrizados | Alta |
| F02 | Frames | Critica |
| F13 | Analisis Estatico (OpenSees) | Critica |
| F18 | Visualizacion Desplazamientos | Critica |
| F19 | Visualizacion Esfuerzos | Critica |
| F21 | Perfiles Extruidos | Alta |
| F33 | Export/Import (incl. AutoCAD) | Media |
| F-UI | Interfaz Usuario | Critica |
| F-FINAL | Integracion | Critica |
| F38 | Compatibilidad macOS | Post-MVP |

---

## Pricing

| Plan | Precio | Target |
|------|--------|--------|
| Estudiante | Gratis | Universidades, pipeline |
| Profesional | $39/mes | Freelancers |
| Equipo (5) | $149/mes | Oficinas pequenas |
| Enterprise | Custom | Grandes consultoras |

**Posicionamiento**: 90% de SAP2000 al 3% del precio

---

## Metricas Objetivo

| Metrica | Target |
|---------|--------|
| Tiempo carga | < 5s |
| Respuesta UI | < 100ms |
| FPS (10k elementos) | > 30 |
| Analisis (10k elementos) | < 30s |
| Memoria maxima | < 4GB |
| Precision vs SAP2000 | >= 99% |

---

## Decisiones Clave

| Decision | Resolucion | Justificacion |
|----------|------------|---------------|
| Arquitectura | Cloud-first (SaaS) | Sin instalacion, sin pirateria, suscripcion |
| Motor | OpenSees + multi-engine | Especializado en estructuras, adaptadores |
| Backend | Python 3.11/3.12 | Compatible con openseespy |
| Frontend | React + Three.js | 3D en browser, multiplataforma |
| Normativas | NCh + AISC + Eurocode | Sin NSR Colombia inicialmente |
| Validacion | vs SAP2000/Robot/RISA | Multiples referencias |
| Enfoque | Solo Analisis | Diseno diferido (complejidad legal) |

---

## Riesgos Principales

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| OpenSees version incompatible | Media | Medio | Python 3.11/3.12 probadas |
| Three.js limitado modelos grandes | Media | Medio | LOD, instancing |
| Scope creep | Alta | Alto | PRD detallado, disciplina |
| Competencia baja precios | Baja | Medio | Diferenciacion: normativas locales |

---

## Equipo

| Rol | Nombre |
|-----|--------|
| Ingeniero Estructural | Pablo |
| Product Manager | Kevin |
| IA de Desarrollo | Claude (Opus 4.5) |

---

## Proyeccion Financiera

| Ano | ARR | Usuarios | Mercado |
|-----|-----|----------|---------|
| 2026 | $72K | 200 | Chile |
| 2027 | $480K | 1,200 | Latam |
| 2028 | $600K | 2,000 | Latam + Europa |

---

## Documentacion

| Documento | Descripcion |
|-----------|-------------|
| BRIEF.md | Vision, objetivos, alcance |
| PRD.md | Features, user stories, requisitos |
| ARQUITECTURA.md | Stack, estructura, patrones |
| feature_list.json | Features ejecutables con steps |
| CLAUDE.md | Instrucciones para desarrollo |
| RETOMAR.md | Estado y proximos pasos |

---

## Estado

**DOCUMENTACION COMPLETA - LISTO PARA IMPLEMENTACION**

El proyecto Strux ha completado su fase de documentacion. Decisiones clave tomadas:
- Cloud-first con React + FastAPI + Three.js
- OpenSees como motor preferido + Kratos alternativo
- Normativas NCh + AISC + Eurocode
- Features diferenciadores: Grillas, Section Designer, Unit Converter
- Validacion automatizada vs SAP2000/Robot/RISA

---

## Proximos Pasos

1. Definir nombre final (Strux, Nifes Forge, Structural Forge)
2. Registrar dominio
3. Crear repositorio GitHub
4. Iniciar implementacion con F00 (Setup)
5. Configurar CI/CD para deploy cloud

---

*Resumen Ejecutivo - Strux*
*Software Profesional de Analisis Estructural*
*Actualizado: 2026-01-04*
