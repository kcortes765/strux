# PRD - PAZ (Product Requirements Document)

**Software Profesional de Analisis Estructural**

Documento: PRD v1.1 (Consolidado)
Fecha: 2026-01-03
Fase: 6.0 - Consolidacion Final

---

## 1. Resumen Ejecutivo

### 1.1 Vision del Producto

PAZ es un software profesional de analisis estructural que democratiza el acceso a herramientas de ingenieria de clase mundial en Latinoamerica. Combina la potencia de SAP2000 con un precio accesible, soporte nativo para normativas regionales y una experiencia movil sincronizada.

El enfoque primario esta en el analisis estructural; las capacidades de diseno se dejan para fases web/movil futuras debido a la complejidad legal de certificaciones y responsabilidades.

### 1.2 Proposito de Este Documento

Este PRD define exhaustivamente las features, user stories, criterios de aceptacion y requisitos tecnicos necesarios para desarrollar PAZ en sus tres fases principales: MVP, V1.0 y V2.0.

### 1.3 Audiencia

- Equipo de desarrollo (Pablo, Kevin, Claude)
- Stakeholders internos
- Futuros contribuidores

### 1.4 Competencia
- **SAP2000** sigue siendo el referente de precision; comparamos resultados para igualar su exactitud y confiabilidad.
- **Robot Structural Analysis** y **RISA** marcan el ritmo en flujos de grillas, combinaciones y chequeos de secciones; documentamos sus ventajas para superarlas con un enfoque centrado en analisis y en interoperabilidad.

### 1.5 Pendientes de Marca
- El nombre "Nifes Forge" esta en evaluacion, se estudia si se mantiene dentro de Nifes o se adopta una alternativa como "Structural Forge" para la linea de productos de analisis estructural.

---

## 2. Features del Producto

### 2.1 Mapa de Features por Fase

| ID | Feature | MVP | V1.0 | V2.0 | Prioridad |
|----|---------|:---:|:----:|:----:|-----------|
| F01 | Modelacion de Nodos | X | X | X | Critica |
| F02 | Modelacion de Frames | X | X | X | Critica |
| F03 | Modelacion de Shells | - | X | X | Alta |
| F04 | Modelacion de Membranas | - | - | X | Media |
| F05 | Modelacion de Cables | - | - | X | Media |
| F06 | Modelacion de Links | - | - | X | Media |
| F07 | Modelacion de Joints | - | - | X | Media |
| F08 | Libreria de Materiales | X | X | X | Critica |
| F09 | Libreria de Secciones AISC | X | X | X | Critica |
| F10 | Libreria de Secciones NCh | - | X | X | Alta |
| F11 | Libreria de Secciones Eurocodigo | - | X | X | Alta |
| F12 | Perfiles Parametrizados | X | X | X | Alta |
| F13 | Analisis Estatico Lineal | X | X | X | Critica |
| F14 | Analisis Dinamico | - | X | X | Alta |
| F15 | Analisis Tiempo-Historia | - | - | X | Alta |
| F16 | Analisis No Lineal | - | - | X | Alta |
| F17 | Modos de Vibrar | - | X | X | Alta |
| F18 | Visualizacion 3D Desplazamientos | X | X | X | Critica |
| F19 | Visualizacion Esfuerzos | X | X | X | Critica |
| F20 | Factores de Utilizacion | - | X | X | Alta |
| F21 | Perfiles Extruidos | X | X | X | Alta |
| F22 | Animacion Modos | - | X | X | Media |
| F23 | Dibujo Dinamico Integrado | - | X | X | Alta |
| F24 | Releases en Frames | - | X | X | Media |
| F25 | Grupos de Elementos | - | X | X | Media |
| F26 | Verificacion Conexiones | - | - | X | Media |
| F27 | Verificacion Fundaciones | - | - | X | Media |
| F28 | Verificacion Momento Volcante | - | - | X | Media |
| F29 | App Movil | - | - | X | Alta |
| F30 | Sincronizacion Cloud | - | - | X | Alta |
| F31 | Gestion de Proyectos | X | X | X | Alta |
| F32 | Sistema de Autenticacion | - | X | X | Alta |
| F33 | Export/Import Formatos | X | X | X | Media |
| F34 | Generacion de Reportes | - | X | X | Media |
| F35 | Sistema de Grillas | X | X | X | Critica |
| F36 | Section Designer | X | X | X | Critica |
| F37 | Conversor de Unidades | X | X | X | Alta |
| F38 | Compatibilidad macOS | - | X | X | Alta |

---

## 3. Especificacion Detallada de Features MVP

### 3.1 F01 - Modelacion de Nodos

**Descripcion**: Crear, editar y eliminar nodos (puntos) en el espacio 3D que definen la geometria de la estructura.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F01-001 | Ingeniero | Crear nodos individuales con coordenadas X, Y, Z | Definir puntos de mi estructura |
| US-F01-002 | Ingeniero | Crear multiples nodos desde un archivo CSV | Importar geometria existente rapidamente |
| US-F01-003 | Ingeniero | Editar coordenadas de nodos existentes | Corregir errores o ajustar geometria |
| US-F01-004 | Ingeniero | Eliminar nodos (con confirmacion si tienen elementos) | Limpiar el modelo |
| US-F01-005 | Ingeniero | Seleccionar nodos con click o ventana de seleccion | Modificar grupos de nodos |
| US-F01-006 | Ingeniero | Ver tabla con todos los nodos y sus propiedades | Revisar la geometria |
| US-F01-007 | Ingeniero | Asignar restricciones (apoyos) a nodos | Definir condiciones de borde |
| US-F01-008 | Ingeniero | Aplicar cargas puntuales a nodos | Simular fuerzas concentradas |

**Criterios de Aceptacion**:

```gherkin
Scenario: Crear nodo individual
  Given el usuario esta en modo modelacion
  When ingresa coordenadas (10, 20, 0) y presiona "Crear Nodo"
  Then se crea un nodo visible en la posicion especificada
  And el nodo aparece en la tabla de nodos

Scenario: Crear nodo duplicado
  Given existe un nodo en (10, 20, 0)
  When el usuario intenta crear otro nodo en (10, 20, 0)
  Then se muestra advertencia de nodo duplicado
  And el usuario puede elegir fusionar o cancelar

Scenario: Eliminar nodo con elementos conectados
  Given existe un nodo con un frame conectado
  When el usuario intenta eliminar el nodo
  Then se muestra confirmacion con lista de elementos afectados
  And el usuario debe confirmar para eliminar nodo y elementos
```

**Requisitos Tecnicos**:
- Precision de coordenadas: 6 decimales
- Tolerancia para nodos duplicados: configurable (default 0.001 unidades)
- Limite de nodos MVP: 50,000

---

### 3.2 F02 - Modelacion de Frames

**Descripcion**: Crear, editar y eliminar elementos lineales (vigas, columnas, arriostramientos) definidos por dos nodos.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F02-001 | Ingeniero | Crear frames seleccionando dos nodos | Definir elementos lineales |
| US-F02-002 | Ingeniero | Crear frames dibujando entre puntos en 3D | Modelar rapidamente sin crear nodos primero |
| US-F02-003 | Ingeniero | Asignar material a un frame | Definir propiedades del material |
| US-F02-004 | Ingeniero | Asignar seccion a un frame | Definir geometria de la seccion |
| US-F02-005 | Ingeniero | Dividir un frame en N segmentos | Refinar el modelo |
| US-F02-006 | Ingeniero | Ver longitud y propiedades de un frame | Verificar el modelo |
| US-F02-007 | Ingeniero | Aplicar cargas distribuidas a frames | Simular pesos propios y sobrecargas |
| US-F02-008 | Ingeniero | Copiar frames con offset | Crear estructuras repetitivas |
| US-F02-009 | Ingeniero | Rotar frames alrededor de su eje | Ajustar orientacion de secciones asimetricas |

**Requisitos Tecnicos**:
- Longitud minima de frame: configurable (default 0.01 unidades)
- Propiedades de frame: area, inercias Ixx/Iyy/Izz, modulo torsional
- Orientacion de ejes locales segun convencion SAP2000

---

### 3.3 F08 - Libreria de Materiales

**Descripcion**: Base de datos de materiales estructurales con propiedades mecanicas predefinidas y capacidad de crear materiales personalizados.

**Materiales Predefinidos MVP**:

| Categoria | Materiales |
|-----------|------------|
| Acero | ASTM A36, A572 Gr50, A992, A500 Gr B/C |
| Hormigon | H20, H25, H30, H35 (NCh), C20, C25, C30, C35 (Eurocodigo) |
| Madera | Pino radiata estructural (NCh) |
| Aluminio | 6061-T6, 6063-T5 |

**Requisitos Tecnicos**:
- Propiedades requeridas: E (modulo elastico), G (modulo corte), nu (Poisson), rho (densidad)
- Propiedades opcionales: fy (fluencia), fu (rotura), alpha (expansion termica)
- Formato de archivo: JSON

---

### 3.4 F09 - Libreria de Secciones AISC

**Descripcion**: Base de datos completa de perfiles de acero segun norma AISC con propiedades geometricas.

**Perfiles AISC Incluidos**:

| Categoria | Tipos | Cantidad aproximada |
|-----------|-------|---------------------|
| W | Wide Flange | ~300 |
| HP | H-Pile | ~20 |
| S | American Standard Beam | ~30 |
| M | Miscellaneous | ~25 |
| C | American Standard Channel | ~20 |
| MC | Miscellaneous Channel | ~20 |
| L | Angle | ~100 |
| WT | Structural Tee (W) | ~150 |
| HSS | Hollow Structural Sections | ~200 |
| PIPE | Standard Pipe | ~15 |
| **Total** | | **~880** |

**Nota sobre fuente de datos**: Los datos de perfiles AISC deben obtenerse de fuente oficial (Manual AISC Steel Construction) o generarse desde formulas geometricas con validacion.

---

### 3.5 F12 - Perfiles Parametrizados

**Descripcion**: Crear secciones personalizadas definiendo dimensiones geometricas parametricas.

**Tipos Parametricos MVP**:

| Tipo | Parametros |
|------|------------|
| I/H | bf, tf, d, tw |
| Rectangular Hueco | B, H, t |
| Circular Hueco | D, t |
| Angulo L | L1, L2, t |
| Canal C | bf, tf, d, tw |
| T | bf, tf, d, tw |
| Rectangular Solido | B, H |
| Circular Solido | D |

---

### 3.6 F13 - Analisis Estatico Lineal

**Descripcion**: Ejecutar analisis estatico lineal del modelo estructural y obtener resultados de desplazamientos y esfuerzos.

**Requisitos Tecnicos**:
- Motor: OpenSees preferido con adaptadores a otros motores (Kratos, Robot, RISA)
- Metodo: Rigidez directa
- Grados de libertad: 6 por nodo (3 traslaciones, 3 rotaciones)
- Precision: double (64-bit)
- Tiempo objetivo: modelo 10,000 elementos < 30 segundos
- Python: versiones 3.11/3.12 compatibles con openseespy para evitar conflictos del engine

---

### 3.7 F18 - Visualizacion 3D de Desplazamientos

**Descripcion**: Mostrar la estructura deformada con escala configurable y coloreado por magnitud.

**Requisitos Tecnicos**:
- Libreria: Three.js (browser)
- FPS minimo: 30 en modelo 10,000 elementos
- Escala de colores: configurable (rainbow, viridis, etc.)
- Interpolacion: lineal entre nodos

---

### 3.8 F19 - Visualizacion de Esfuerzos

**Descripcion**: Mostrar diagramas de esfuerzos internos en elementos con coloreado por magnitud.

**Esfuerzos Disponibles MVP**:

| Codigo | Descripcion |
|--------|-------------|
| P | Fuerza axial |
| V2 | Corte en eje 2 |
| V3 | Corte en eje 3 |
| T | Torsion |
| M2 | Momento alrededor de eje 2 |
| M3 | Momento alrededor de eje 3 |

---

### 3.9 F21 - Perfiles Extruidos

**Descripcion**: Visualizar elementos frame con su geometria de seccion real (3D solido) en lugar de lineas.

**Requisitos Tecnicos**:
- Geometria: mesh por seccion, extruido a lo largo del eje
- LOD (Level of Detail): configurable segun zoom
- Optimizacion: instancing para secciones repetidas

---

### 3.10 F31 - Gestion de Proyectos

**Descripcion**: Crear, guardar, abrir y gestionar proyectos estructurales.

**Requisitos Tecnicos**:
- Formato de archivo: .paz (JSON comprimido con gzip)
- Tamano tipico: < 10MB para modelo 10,000 elementos
- Compatibilidad: versionado de formato

**Nota**: JSON es el formato nativo del proyecto (.paz), no un formato de intercambio. Los formatos de intercambio son CSV y DXF.

---

### 3.11 F33 - Export/Import Formatos

**Descripcion**: Exportar e importar modelos en formatos estandar para interoperabilidad, incluyendo la conversión de lineas AutoCAD a nodos/frames y la sincronizacion con el modelo SAP/PAZ.

**Formatos MVP**:

| Formato | Import | Export | Descripcion |
|---------|:------:|:------:|-------------|
| CSV | X | X | Nodos, elementos, resultados |
| DXF | X | X | Geometria 3D |

**Importador AutoCAD**:

- Lineas DXF que representan ejes o perfiles se convierten automaticamente en nodos y frames sap.
- El usuario puede mapear capas de AutoCAD a materiales y secciones de la libreria.
- Se mantiene la coherencia de unidades aprovechando el conversor rapido (F37).

**Criterios de Aceptacion**:

- Importador DXF crea nodos/frames que coinciden con las lineas de AutoCAD y respeta capas y materiales asignados.
- Exportaciones CSV y DXF guardan propiedades completas y pueden reimportarse sin perdida.
- Se puede transformar una linea AutoCAD en un elemento SAP/PAZ en un maximo de tres clics.

**Nota**: El formato JSON (.paz) es el formato nativo del proyecto, no un formato de intercambio separado.

---

### 3.12 F35 - Sistema de Grillas

**Descripcion**: Superponer grillas parametricas que ayudan a orientar nodos y frames durante la modelacion y que se pueden activar, personalizar y usar como referencia de snapping.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F35-001 | Ingeniero | Activar o ocultar una grilla mayor y menor en el viewport | Referenciar rapidamente la geometria |
| US-F35-002 | Ingeniero | Definir separacion de grilla por eje y unidades | Trabajar en escalas locales sin alterar el modelo |
| US-F35-003 | Ingeniero | Forzar que nodos y frames nuevos se alineen a la grilla cuando el snapping esta activo | Evitar errores de posicionamiento |

**Criterios de Aceptacion**:

- Grid visible con atajos y puede activarse/desactivarse sin recargar el modelo.
- Las dimensiones de la grilla (mayor/menor) son configurables y se guardan en el proyecto.
- El snapping a grilla se puede encender/apagar y respeta tolerancias por eje.

**Requisitos Tecnicos**:

- Layer de grilla renderizado en viewport con lineas mayor/minor y reticula 3D.
- Servicio de grid configura el spacing en unidades definidas por el usuario y actualiza la vista inmediatamente.
- Snapping usa la tolerancia de `core/units` y admite redondeo a multiplos de la grilla.

### 3.13 F36 - Section Designer

**Descripcion**: Herramienta para crear y ajustar secciones mixtas o no estandar definiendo perfiles compuestos, dimensiones personalizadas y materiales activos.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F36-001 | Ingeniero | Crear una seccion personalizada desde cero ingresando dimensiones y materiales | Modelar perfiles no comerciales |
| US-F36-002 | Ingeniero | Combinar geometria de acero y hormigon en una seccion y ver sus propiedades automaticamente | Validar secciones mixtas |
| US-F36-003 | Ingeniero | Guardar la seccion creada en la libreria del proyecto y reutilizarla | Escalar modelos repetitivos |

**Criterios de Aceptacion**:

- Se pueden definir dimensiones, materiales y capas de una seccion y obtener area, inercias y propiedades de torsion.
- Las secciones creadas generan `shape_data` que permiten su renderizado/extrusion en el viewport.
- Se pueden guardar como plantillas y exportarse a JSON del proyecto.

**Requisitos Tecnicos**:

- Section Designer valida dimensiones para evitar geometria invalida y calcula automaticamente E, G, Ixx, Iyy, rx, ry.
- Serializa la seccion en el formato ya usado por `sections_repository` y la hace disponible para frames y extrusiones.
- Genera `shape_data` con vertices para que el renderizador pueda extruir la seccion en 3D.

### 3.14 F37 - Conversor de Unidades

**Descripcion**: Panel rapido de conversiones para cambiar fuerzas y longitudes (kN<->tonelada, kip<->kN, m<->ft) sin abandonar el flujo del analisis.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F37-001 | Ingeniero | Convertir una carga de kN a toneladas en un cuadro de dialogo | Verificar entrada en unidades del cliente |
| US-F37-002 | Ingeniero | Copiar el resultado de una conversion rapida a la pantalla de cargas o resultados | Evitar errores de reescritura |
| US-F37-003 | Ingeniero | Recordar mis unidades preferidas y aplicarlas en el viewport y tablas | Minimizar ajustes manuales |

**Criterios de Aceptacion**:

- Panel muestra conversiones para kN, ton, kip, m, ft, kgf y lb con precision configurada.
- Los resultados se pueden copiar y pegar en formularios de carga o en tablas de resultados.
- El sistema respeta la configuracion del proyecto (metros, pies, etc.).

**Requisitos Tecnicos**:

- Servicio de conversion (`UnitConversionService`) reutiliza `core/units` y expone multiplicadores para la UI.
- Panel ofrece botones rapidos (kN<->tonelada, kip<->kN, m<->ft) y un campo libre para otras conversiones.
- Logger documenta cada conversion para auditoria.

### 3.15 F38 - Compatibilidad macOS

**Descripcion**: Validar y empaquetar el MVP para macOS, asegurando que rutas de archivo, dependencias y wrappers se comporten igual que en Windows antes de lanzar la version publicitaria.

**User Stories**:

| US-ID | Como... | Quiero... | Para... |
|-------|---------|-----------|---------|
| US-F38-001 | Ingeniero Mac | Tener un instalador/corriendo similar al de Windows | Trabajar con el mismo flujo de analisis |
| US-F38-002 | Ingeniero | Verificar que las dependencias Python y OpenSees compilan en macOS sin conflictos | Evitar bugs de plataforma |
| US-F38-003 | DevOps | Generar builds automatizados para macOS que incluyan pruebas basicas | Mantener calidad release |

**Criterios de Aceptacion**:

- Existe un build funcional en macOS que ejecuta el flujo: crear proyecto -> modelar -> correr analisis -> ver resultados.
- Las dependencias (OpenSees, Python 3.11+) se instalan y ejecutan sin errores en mac.
- Hay documentacion para replicar el setup en macOS (instalador o script de empaquetado).

**Requisitos Tecnicos**:

- El backend y el empaquetado (PyInstaller/Nuitka) soportan macOS y se liberan binarios firmados si es posible.
- El frontend React y Three.js se verifican en Safari/Chromium sobre macOS.
- La integracion con OpenSees usa bindings compatibles y se prueban en Apple Silicon/Intel.

---

## 4. Requisitos No Funcionales

### 4.1 Rendimiento

| ID | Requisito | Metrica | Target |
|----|-----------|---------|--------|
| RNF-001 | Tiempo de carga inicial | Segundos | < 5s |
| RNF-002 | Respuesta UI | Milisegundos | < 100ms |
| RNF-003 | Render 3D (10k elementos) | FPS | > 30 |
| RNF-004 | Analisis estatico (10k elementos) | Segundos | < 30s |
| RNF-005 | Memoria maxima | GB | < 4GB |
| RNF-006 | Tamano instalador | MB | < 500MB |

### 4.2 Usabilidad

| ID | Requisito | Descripcion |
|----|-----------|-------------|
| RNF-007 | Consistencia UI | Mismos patrones de interaccion en toda la app |
| RNF-008 | Shortcuts de teclado | Atajos para operaciones frecuentes |
| RNF-009 | Undo/Redo | Minimo 50 niveles |
| RNF-010 | Tooltips | Ayuda contextual en todos los botones |
| RNF-011 | Mensajes de error | Claros, accionables, sin jerga tecnica |
| RNF-012 | Feedback visual | Indicadores de progreso para operaciones largas |

### 4.3 Compatibilidad

| ID | Requisito | Descripcion |
|----|-----------|-------------|
| RNF-013 | Windows 10/11 y macOS (futura) | Soporte completo en Windows, hoja de ruta para compatibilidad macOS |
| RNF-014 | Resoluciones | 1920x1080 minimo, soporte HiDPI |
| RNF-015 | Sin dependencias externas | Instalador standalone |
| RNF-016 | Idioma inicial | Espanol e Ingles |
| RNF-024 | Python 3.11/3.12 | Versiones alineadas con openseespy y dependencias del engine |

### 4.4 Seguridad

| ID | Requisito | Descripcion |
|----|-----------|-------------|
| RNF-017 | Datos locales | Archivos almacenados localmente |
| RNF-018 | Sin telemetria | No enviar datos sin consentimiento |
| RNF-019 | Validacion de archivos | Verificar integridad al abrir |

### 4.5 Mantenibilidad

| ID | Requisito | Descripcion |
|----|-----------|-------------|
| RNF-020 | Arquitectura modular | Separacion clara de capas |
| RNF-021 | Tests automatizados | > 80% cobertura en core |
| RNF-022 | Documentacion codigo | Docstrings en funciones publicas |
| RNF-023 | Logs de errores | Sistema de logging para debugging |

---

## 5. Integraciones

### 5.1 Motor de Calculo

**OpenSees (preferido) con adaptador multi-motor**

| Aspecto | Detalle |
|---------|---------|
| Tipo | openseespy bindings Python |
| Comunicacion | API Python directa y adaptadores para Kratos/otros |
| Licencia | Open Source (OpenSees) y BSD (Kratos) |
| Elementos soportados | Frame, Shell, Solid, arco/elementos compuestos |
| Analisis soportados | Estatico, Dinamico, Tiempo-historia, No lineal (multi-motor) |

### 5.2 Visualizacion

**Three.js (frontend web)**

| Aspecto | Detalle |
|---------|---------|
| Version | Three.js latest |
| Funcionalidades | Mesh rendering, picking, orbit controls |
| Integracion | React component |

### 5.3 Validacion

**SAP2000 API (testing)**

| Aspecto | Detalle |
|---------|---------|
| Proposito | Validar resultados de Kratos vs estandar industria |
| Comunicacion | OAPI via comtypes (Python) |
| Uso | Solo en CI/CD, no en produccion |

---

## 6. Dependencias Entre Features

### 6.1 Mapa de Dependencias

```
F00 (Setup) --> F31 (Proyectos) --> F01 (Nodos) --> F08 (Materiales)
                                                 --> F09 (AISC) --> F12 (Param)
                                                                 --> F02 (Frames)

F02 (Frames) --> F13 (Analisis) --> F18 (Desplazamientos) --> F19 (Esfuerzos)
                                                           --> F21 (Extruidos)
                                                           --> F33 (Export/Import)

F33 --> F-UI (Interfaz) --> F-FINAL (Integracion)
```

### 6.2 Orden de Implementacion MVP (Feature List)

1. F00 - Setup del Proyecto
2. F31 - Gestion de Proyectos
3. F01 - Nodos
4. F08 - Materiales
5. F09 - Secciones AISC
6. F12 - Perfiles Parametrizados
7. F02 - Frames
8. F13 - Analisis Estatico
9. F18 - Visualizacion Desplazamientos
10. F19 - Visualizacion Esfuerzos
11. F21 - Perfiles Extruidos
12. F33 - Export/Import
13. F-UI - Interfaz Usuario
14. F-FINAL - Integracion y Polish

**Nota**: Este orden difiere ligeramente del orden conceptual del PRD porque considera dependencias tecnicas. F02 (Frames) se implementa despues de F12 (Parametrizados) porque requiere secciones.

---

## 7. Criterios de Aceptacion Globales

### 7.1 Definition of Done

Una feature se considera completa cuando:

1. **Codigo**: Implementado y revisado
2. **Tests**: Unitarios y de integracion pasando
3. **Documentacion**: Actualizada
4. **UX**: Validada con 1+ usuario
5. **Performance**: Dentro de metricas objetivo
6. **Sin bugs**: Criticos o bloqueantes

### 7.2 Definition of Ready

Una feature esta lista para desarrollo cuando:

1. **User Stories**: Definidas y aceptadas
2. **Criterios de Aceptacion**: Claros y medibles
3. **Dependencias**: Identificadas y resueltas
4. **Diseno**: Wireframes/mockups aprobados (si aplica)
5. **Estimacion**: Esfuerzo estimado

---

## 8. Glosario Tecnico

| Termino | Definicion |
|---------|------------|
| Frame | Elemento estructural lineal (viga, columna, arriostramiento) |
| Shell | Elemento estructural de superficie (losa, muro) |
| Nodo | Punto en el espacio que define geometria y tiene grados de libertad |
| DOF | Degrees of Freedom - grados de libertad (traslaciones y rotaciones) |
| Mesh | Discretizacion de la estructura en elementos finitos |
| Modal | Analisis de frecuencias naturales y modos de vibrar |
| Release | Liberacion de grados de libertad en extremo de frame |
| Factor de Utilizacion | Ratio demanda/capacidad de un elemento |
| Section | Propiedades geometricas y mecanicas de una seccion transversal |
| Engine | Motor de calculo (solver) para analisis estructural |
| NCh | Norma Chilena |
| OpenSees | Framework de analisis estructural especifico (openseespy) |
| AISC | American Institute of Steel Construction |

---

## 9. Trazabilidad

### 9.1 Matriz de Trazabilidad Requisitos -> Features

| Requisito INPUT.md | Feature PRD | Feature List | Cobertura |
|--------------------|-------------|--------------|-----------|
| Nodos | F01 | F01 | 100% |
| Frames | F02 | F02 | 100% |
| Materiales libreria | F08 | F08 | 100% |
| Secciones AISC | F09 | F09 | 100% |
| Perfiles parametrizados | F12 | F12 | 100% |
| Analisis estatico lineal | F13 | F13 | 100% |
| Visualizacion desplazamientos | F18 | F18 | 100% |
| Visualizacion esfuerzos | F19 | F19 | 100% |
| Perfiles extruidos | F21 | F21 | 100% |
| Gestion proyectos | F31 | F31 | 100% |
| Export/Import | F33 | F33 | 100% |

---

*PRD consolidado - Fase 6.0 DocGen*
*Proyecto PAZ - Software Profesional de Analisis Estructural*
