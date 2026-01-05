# RETOMAR.md - PAZ

> **TL;DR**: Proyecto PAZ está en fase de documentación. Ejecutar `agente.ps1 -All` desde `DocGen/` para generar BRIEF, PRD y ARQUITECTURA. Output en `6-final/`.

> Lee este archivo primero si eres una IA nueva trabajando en este proyecto.

---

## Quick Start

```powershell
cd "C:\Seba\PAZ\DocGen"
& 'C:\Seba\agente.ps1' -All
```

**Éxito**: 4 archivos en `6-final/` (BRIEF.md, PRD.md, ARQUITECTURA.md, feature_list.json).
**Error**: Ver sección [Si Falla](#si-falla).

---

## Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | PAZ (en evaluación: Nifes Forge / Structural Forge) |
| **Tipo** | Cloud SaaS (React + FastAPI + OpenSees/Kratos) |
| **Estado** | DOCUMENTACIÓN COMPLETADA - LISTO PARA CODIFICAR |
| **Motor** | OpenSees (preferido) + Kratos (alternativo) |
| **Normativas** | NCh + AISC + Eurocode (sin NSR) |
| **Última actividad** | 2026-01-04 |

---

## Leer Primero

| Orden | Archivo | Propósito |
|-------|---------|-----------|
| 1 | `DocGen/INPUT.md` | Contexto completo del proyecto (242 líneas). |
| 2 | `.agente/conversacion/resumen.md` | Estado acumulado (si existe). |
| 3 | `DocGen/CLAUDE.md` | Instrucciones de DocGen. |

**Obligatorio**: Leer al menos INPUT.md antes de ejecutar.

---

## Estado Actual

### Sistema DocGen Configurado

- Engine en: `C:\Seba\DocGen\`.
- Proyecto en: `C:\Seba\PAZ\DocGen\`.
- INPUT.md completado con transcripción de planificación.
- 7 fases listas para ejecutar.

### Pendiente

Ejecutar DocGen para generar:
- Brief del proyecto.
- PRD exhaustivo.
- Arquitectura técnica.
- feature_list.json para desarrollo.

---

## Prerrequisitos

### Verificaciones Obligatorias

Ejecutar ANTES de la tarea principal. Si alguna falla, NO continuar.

```powershell
# 1. Verificar engine existe
Test-Path "C:\Seba\DocGen\"
# Esperado: True. Si False: El engine no está instalado.

# 2. Verificar INPUT.md tiene contenido
(Get-Content "C:\Seba\PAZ\DocGen\INPUT.md" -ErrorAction Stop).Count -gt 100
# Esperado: True. Si False: INPUT.md está vacío o incompleto.

# 3. Verificar feature_list.json existe y es JSON válido
Get-Content "C:\Seba\PAZ\DocGen\feature_list.json" | ConvertFrom-Json
# Esperado: Objeto JSON. Si error: JSON corrupto.

# 4. Verificar agente.ps1 existe
Test-Path "C:\Seba\agente.ps1"
# Esperado: True. Si False: Script no instalado.
```

### Si un Prerrequisito Falla

| Prerrequisito | Si falla | Acción |
|---------------|----------|--------|
| Engine no existe | `Test-Path` = False | Clonar/copiar `C:\Seba\DocGen\` desde backup. |
| INPUT.md vacío | <100 líneas | Revisar transcripción original, regenerar INPUT.md. |
| JSON corrupto | Error de parse | Restaurar feature_list.json desde template o backup. |
| agente.ps1 no existe | `Test-Path` = False | Verificar ruta correcta en `C:\Seba\`. |

### Archivos Requeridos

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `INPUT.md` | `DocGen/INPUT.md` | Contexto completo del proyecto. |
| `feature_list.json` | `DocGen/feature_list.json` | 7 fases de DocGen. |
| `agente.ps1` | `C:\Seba\agente.ps1` | Engine de ejecución. |

### Software Necesario

- **PowerShell 5.0+**: Para ejecutar agente.ps1.
- **Claude Code**: Con API configurada (`$env:ANTHROPIC_API_KEY`).
- **Git**: Para control de versiones (opcional pero recomendado).

---

## Próxima Tarea

### Comando

```powershell
cd "C:\Seba\PAZ\DocGen"
& 'C:\Seba\agente.ps1' -All
```

### Qué Hace

Ejecuta las 7 fases de DocGen secuencialmente:
1. Análisis de INPUT.md.
2. Generación de BRIEF.md.
3. Generación de PRD.md.
4. Generación de ARQUITECTURA.md.
5. Generación de feature_list.json de desarrollo.
6. Revisión cruzada.
7. Consolidación en `6-final/`.

### Tiempo Esperado

- **Normal**: 45-90 minutos.
- **Timeout**: Si >3 horas sin output, considerar fallo.

---

## Verificación de Éxito

### Checklist de Archivos Generados

Después de ejecutar, verificar que existan en `6-final/`:

| Archivo | Tamaño Mínimo | Contenido Esperado | Estado |
|---------|---------------|-------------------|--------|
| `BRIEF.md` | >100 líneas | Visión, objetivos, alcance, stakeholders. | ☐ |
| `PRD.md` | >400 líneas | Features, user stories, criterios de aceptación. | ☐ |
| `ARQUITECTURA.md` | >300 líneas | Stack, estructura, modelo de datos. | ☐ |
| `feature_list.json` | JSON válido | Array de features con id, name, steps. | ☐ |

**Tolerancia**: ±10% en líneas es aceptable (ej: 90 líneas en BRIEF = OK).

### Comando de Verificación

```powershell
# Verificar existencia y tamaño
Get-ChildItem "C:\Seba\PAZ\DocGen\6-final\" |
    Select-Object Name, @{N='Lines';E={(Get-Content $_.FullName).Count}}

# Validar JSON
Get-Content "C:\Seba\PAZ\DocGen\6-final\feature_list.json" | ConvertFrom-Json |
    Select-Object -ExpandProperty features | Measure-Object
```

### Próximo Paso Después del Éxito

1. Revisar documentos en `6-final/`.
2. Actualizar este RETOMAR.md: cambiar Estado a "DOCUMENTACIÓN COMPLETA".
3. Mover tarea al Historial.
4. Ejecutar `/preparar-auto` para setup de codificación.

---

## Si Falla

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `agente.ps1 not found` | Ruta incorrecta. | Verificar: `Test-Path "C:\Seba\agente.ps1"`. |
| `Rate limit de API` | Cuota agotada. | Esperar reset automático (~1 hora). El script reintenta. |
| `INPUT.md empty` | Archivo sin contenido. | Verificar: `(Get-Content INPUT.md).Count -gt 100`. |
| `JSON parse error` | feature_list.json corrupto. | Restaurar desde backup o regenerar. |
| `Fase X falla` | Dependencia no completada. | Verificar feature_list.json, ejecutar en orden. |
| `Timeout > 3 hrs` | Sesión colgada o API no responde. | Cancelar y reintentar: `agente.ps1 -All`. |
| `Permiso denegado` | Sin acceso a directorio. | Ejecutar PowerShell como Administrador. |
| `401 Unauthorized` | API key inválida o expirada. | Verificar: `$env:ANTHROPIC_API_KEY`. |

### Idempotencia

**Sí es seguro reintentar**. El script:
- Retoma donde se quedó (features con `passes: false`).
- No duplica trabajo completado.
- Reintenta automáticamente (máx 3 veces por fase).

### Dónde Ver Logs

```powershell
# Ver estado actual
& 'C:\Seba\agente.ps1' -Status

# Ver memoria acumulada
& 'C:\Seba\agente.ps1' -Memoria

# Ver feature_list.json actual
Get-Content "C:\Seba\PAZ\DocGen\feature_list.json" | ConvertFrom-Json |
    Select-Object -ExpandProperty features | Format-Table id, name, passes
```

### Cuándo Escalar a Humano

1. Error persistente después de 3 reintentos.
2. INPUT.md contradictorio o incompleto (requiere clarificación de Pablo/Kevin).
3. Fase específica falla consistentemente.
4. API key inválida (requiere acceso a cuenta Anthropic).

### Documentar Error

Si falla, agregar esta sección antes de cerrar:

```markdown
### ERROR [YYYY-MM-DD HH:mm]

**Fase**: [0.1 | 1.0 | 2.0 | 3.0 | 4.0 | 5.0 | 6.0]
**Error**: [Mensaje exacto del error]
**Acción tomada**: [Qué se intentó]
**Próximo paso**: [Qué debe hacer la siguiente IA/humano]
```

---

## Decisiones Importantes

| Decisión | Valor | Razón | Reversible |
|----------|-------|-------|------------|
| Arquitectura | Cloud-first (SaaS) | Sin instalación, sin piratería, suscripción fácil. | No. |
| Motor de cálculo | OpenSees (preferido) + multi-engine | Especializado en estructuras, con adaptadores para Kratos/RISA. | Sí (cambiar motor). |
| Backend | Python 3.11/3.12 + FastAPI | Versiones compatibles con openseespy. | No. |
| Frontend | React + Three.js | 3D en browser, multiplataforma. | No. |
| Validación | vs SAP2000/Robot/RISA (API) | Múltiples referencias de la industria. | N/A. |
| Normativas | NCh + AISC + Eurocode | Sin NSR Colombia por ahora. | Sí (agregar NSR). |
| Features nuevos | Grillas, Section Designer, Unit Converter | Diferenciadores clave vs competencia. | N/A. |
| macOS | Soporte en V1.0 | Hoja de ruta clara. | N/A. |
| Pagos | Stripe | Suscripciones automáticas. | Sí. |
| Nombre | Pendiente: PAZ, Nifes Forge, Structural Forge | En evaluación. | Sí. |

---

## Estructura

```
C:\Seba\PAZ\
├── RETOMAR.md                  ← ESTE ARCHIVO
├── .agente/
│   └── conversacion/
│       ├── resumen.md          ← Estado acumulado
│       └── reciente.md         ← Última sesión
├── DocGen/                     ← SISTEMA DE DOCUMENTACIÓN (usar este)
│   ├── INPUT.md                ← Data del proyecto (242 líneas)
│   ├── feature_list.json       ← 7 fases
│   ├── CLAUDE.md               ← Instrucciones
│   ├── 0-analisis/ ... 5-revision/  ← Outputs intermedios
│   └── 6-final/                ← OUTPUT FINAL
└── DeepResearch/               ← Sistema de investigación web (NO usar para esta tarea)
```

---

## Stakeholders

| Rol | Nombre | Responsabilidad | Contactar si... |
|-----|--------|-----------------|-----------------|
| Ingeniero Estructural | Pablo | Define requisitos técnicos y validación de ingeniería. | Dudas sobre funcionalidad estructural. |
| Product Manager | Kevin | Arquitectura, gestión y decisiones de negocio. | Dudas sobre prioridades o alcance. |

---

## Herramientas

| Herramienta | Ubicación | Propósito |
|-------------|-----------|-----------|
| DocGen | `C:\Seba\DocGen\` | Sistema de generación de documentación (7 fases). |
| agente.ps1 | `C:\Seba\agente.ps1` | Engine de ejecución automática headless. |
| LSP | Integrado en Claude Code | Navegación de código (900x más rápido que grep). |

---

## Historial

| Fecha | Sesión | Acción | Resultado |
|-------|--------|--------|-----------|
| 2026-01-03 | S001 | Configuración inicial de DocGen. | Completado. |
| 2026-01-03 | S001 | Extracción de contexto desde transcripción. | Completado. |
| 2026-01-03 | S002 | Revisión y mejora de RETOMAR.md (v1). | Completado. |
| 2026-01-03 | S003 | Auditoría con 5 agentes + mejoras finales (v2). | Completado. |

---

## Glosario

### Motores de Cálculo

| Término | Definición |
|---------|-----------|
| **OpenSees** | Motor preferido de PAZ. Especializado en análisis estructural. Python 3.11/3.12. |
| **Kratos** | Motor alternativo. Licencia BSD, comercialmente viable. |

### Stack Tecnológico

| Término | Definición |
|---------|-----------|
| **FastAPI** | Framework Python para APIs de alto rendimiento. Backend de PAZ. |
| **React** | Librería JavaScript para interfaces de usuario. Frontend de PAZ. |
| **Three.js** | Librería JavaScript para visualización 3D en browser. |
| **Stripe** | Pasarela de pagos para suscripciones. |

### Features Diferenciadores

| Término | Definición |
|---------|-----------|
| **GridManager** | Sistema de grillas parametricas para modelación estructurada. |
| **SectionDesigner** | Editor de secciones mixtas y no estándar (tipo SAP2000). |
| **UnitConverter** | Conversor rápido de unidades estilo Mathcad (kN↔ton, m↔ft). |
| **AutoCADImporter** | Importador de líneas desde DXF a nodos/frames. |

### Documentación

| Término | Definición |
|---------|-----------|
| **PRD** | Product Requirements Document. Especificación de requerimientos del software. |
| **DocGen** | Sistema automático de generación de documentación técnica en 7 fases. |
| **BRIEF** | Documento ejecutivo con visión, objetivos y alcance del proyecto. |

### Sistema de Automatización

| Término | Definición |
|---------|-----------|
| **agente.ps1** | Script PowerShell que ejecuta Claude Code en modo automático headless. |
| **feature_list.json** | Archivo JSON que define las tareas/fases a ejecutar y su estado (`passes`). |

### Dominio Estructural

| Término | Definición |
|---------|-----------|
| **SAP2000** | Software comercial de referencia. PAZ busca funcionalidad equivalente. |
| **Frame** | Elemento estructural tipo pórtico. Resistente a flexión y corte. |
| **Shell** | Elemento bidimensional para placas y láminas. |
| **AISC** | American Institute of Steel Construction. Normativa de acero estadounidense. |
| **NCh** | Norma Chilena de diseño estructural. |

---

*Guardado: 2026-01-04 | Versión: 4.0 | Cambio: OpenSees preferido + multi-engine + Grillas + Section Designer + Eurocode*
