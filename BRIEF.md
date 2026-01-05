# Brief del Proyecto - PAZ

**Software Profesional de Analisis Estructural**

Documento: Brief v1.1 (Consolidado)
Fecha: 2026-01-03
Fase: 6.0 - Consolidacion Final

---

## 1. Vision del Producto

### 1.1 Declaracion de Vision

**PAZ** sera el software de analisis estructural de referencia en Latinoamerica: una herramienta profesional, moderna y economicamente accesible que democratiza el acceso a tecnologia de ingenieria estructural de clase mundial.

### 1.2 Propuesta de Valor Unica

| Problema del Mercado                                         | Solucion PAZ                                                                                 |
|--------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| Licencias prohibitivas ($5,000-$15,000 USD/ano)              | Precio accesible para mercado Latam                                                         |
| Normativas regionales y europeas dispersas y costosas        | Soporte nativo NCh (Chile), AISC (estandar general) y Eurocodigos desde el primer alfa       |
| Herramientas enfocadas en diseno, no en analisis profundo    | Analisis centrado, grillas integradas y Section Designer para secciones mixtas o no estandar |
| Interoperabilidad limitada y conversion de unidades lenta    | Importador de lineas AutoCAD/SAP y conversores rapidos kN<->ton comparables a Mathcad/SAP     |
| Dependencia de un solo motor sin opciones                    | OpenSees como motor preferido, pero arquitectura abierta que permite elegir otro motor       |

### 1.3 Posicionamiento

> "PAZ es para ingenieros estructurales lo que Figma fue para disenadores: una alternativa moderna, accesible y colaborativa a las herramientas legacy del mercado."

**Diferenciadores clave:**
1. **Costo + cumplimiento normativo**: Precio accesible con soporte nativo NCh (Chile), AISC y Eurocodigos desde el inicio y caminos claros para mas normas.
2. **Analisis y modelado enfocado**: Flujo de analisis como prioridad, grillas inteligentes y un Section Designer que cubre perfiles mixtos o no estandar antes que funcionalidades de diseno complicadas.
3. **Interoperabilidad y conversion**: Importador de lineas desde AutoCAD a modelos SAP/PAZ y conversores de unidades estilo Mathcad/SAP (kN<->ton, kip<->kN, etc.) lista para usar.
4. **Arquitectura abierta y multiplataforma**: Motor preferido OpenSees con opcion de cambiar a otro solver, backend Python alineado con versiones compatibles y hoja de ruta clara para extender soporte a macOS.

### 1.4 Competencia
- **SAP2000 (CSI)** mantiene el liderazgo por su precision y ecosistema; automatizamos benchmarking para igualar sus resultados y generar confianza.
- **Robot Structural Analysis** aporta flujos solidos de grillas y combinaciones, mientras que **RISA** sobresale en evaluaciones rapidas de secciones; los analizamos para superarlos con un enfoque abierto al analisis, interoperabilidad y mejoras de UX.

---

## 2. Objetivos SMART

### 2.1 Objetivos de Producto

| ID | Objetivo | Especifico | Medible | Alcanzable | Relevante | Tiempo |
|----|----------|------------|---------|------------|-----------|--------|
| OBJ-01 | Lanzar MVP funcional | Analisis estatico lineal con visualizacion 3D | Modelo de 1000+ elementos calculado correctamente | Si, stack definido | Core del producto | 6 meses |
| OBJ-02 | Precision de calculo | Resultados identicos a SAP2000 en casos base | >= 99% correlacion en benchmark | Si, OpenSees validado con comparaciones a Robot/RISA | Credibilidad profesional | 6 meses |
| OBJ-03 | Rendimiento competitivo | Tiempo de calculo comparable | <= 2x tiempo SAP2000 | Si, PyVista optimizado | UX profesional | 6 meses |

### 2.2 Objetivos de Negocio

| ID | Objetivo | Especifico | Medible | Alcanzable | Relevante | Tiempo |
|----|----------|------------|---------|------------|-----------|--------|
| OBJ-04 | Validacion de mercado | Usuarios beta activos | >= 50 usuarios beta | Si, red de contactos | Product-market fit | 9 meses |
| OBJ-05 | Modelo comercial | Generar ingresos | Primera venta realizada | Si, precio atractivo | Sostenibilidad | 12 meses |
| OBJ-06 | Expansion regional | Usuarios fuera de Chile | >= 10 usuarios Colombia/Peru | Si, normativas soportadas | Crecimiento | 18 meses |

### 2.3 Objetivos Tecnicos

| ID | Objetivo | Especifico | Medible | Alcanzable | Relevante | Tiempo |
|----|----------|------------|---------|------------|-----------|--------|
| OBJ-07 | Motor comercializable | Motor con licencia viable | OpenSees funcional con adaptadores multi-motor | Si, licencia BSD/compatible | Comercializacion | 6 meses |
| OBJ-08 | Distribuible standalone | Ejecutable sin dependencias externas | .exe Windows funcional | Si, Nuitka | Distribucion | 6 meses |
| OBJ-09 | App movil sincronizada | Complemento movil operativo | iOS + Android funcional | Si, framework por definir | Diferenciacion | 15 meses |

---

## 3. Alcance del Proyecto

### 3.1 Dentro del Alcance (In-Scope)

#### MVP (0-2 meses)
| Categoria | Features |
|-----------|----------|
| **Modelacion** | Nodos, Frames, grillas parametricas y Section Designer para perfiles mixtos/no estandar, materiales/secciones basicos |
| **Librerias** | AISC (~880 perfiles), librerias NCh y Eurocodigos, perfiles parametrizados basicos |
| **Analisis** | Analisis estatico lineal con OpenSees preferido (motor intercambiable) y validacion continua contra SAP2000/Robot/RISA |
| **Visualizacion** | 3D con Three.js, deformada, diagramas de esfuerzos y overlay de grillas |
| **Interoperabilidad y Unidades** | Importador de lineas AutoCAD a SAP/PAZ y conversores rapidos kN<->ton, kip<->kN, m<->ft estilo Mathcad |
| **Plataforma** | Cloud (web) con responsividad y hoja de ruta para compatibilidad macOS futura |
| **Formato** | Formato nativo .paz (JSON) |

#### V1.0 (6-12 meses)
| Categoria | Features |
|-----------|----------|
| **Modelacion** | Shells, releases, grupos, dibujo dinamico, grillas avanzadas y Section Designer para secciones no estandar |
| **Librerias** | Cobertura completa NCh y Eurocodigos, actualizacion constante de AISC, secciones mixtas en librerias parametricas |
| **Analisis** | Dinamico, modos de vibrar, combinaciones automatizadas y selector de motor (OpenSees/Kratos) con validacion cruzada |
| **Visualizacion** | Animacion de modos, coloreado por componentes, overlay de grillas y paneles de resultados sincronizados |
| **Verificacion** | Factores de utilizacion y chequeos normativos para NCh/AISC/Euro |
| **Interoperabilidad** | Mejora del importador AutoCAD, exportador a SAP y flujo de conversiones de unidades estilo Mathcad/SAP |
| **Plataforma** | macOS en beta + mejoras del stack cloud y pipelines de build |

#### V2.0 (12-18 meses)
| Categoria | Features |
|-----------|----------|
| **Modelacion** | Membranas, cables, links, joints y refinamiento de grillas con Section Designer para secciones compuestas |
| **Librerias** | Librerias de normas adicionales en Europa/Latam, datos de secciones mixtas y perfiles compuestos |
| **Analisis** | Tiempo-historia, no lineal y verificacion multiengine con combinaciones normativas |
| **Verificacion** | Conexiones, fundaciones, momento volcante y chequeos cruzados NCh/AISC/Euro |
| **Movil** | App sincronizada con calculadoras de cargas, conversion de unidades y acceso a resultados clave |
| **Cloud** | Sincronizacion desktop-movil y despliegue a nuevos mercados con normativas ampliadas |

### 3.2 Fuera del Alcance (Out-of-Scope)

| Item | Razon | Alternativa |
|------|-------|-------------|
| Diseno de estructuras completo | Enfoque en analisis; diseno legalmente complejo queda para una fase web/movil futura | Exportar a software de diseno |
| BIM completo / IFC nativo | Complejidad excesiva | Importar geometria simplificada |
| Analisis geotecnico avanzado | Fuera del core | Integracion futura con software especializado |
| Renderizado fotorrealista | No aporta valor a ingenieros | Exportar a software de render |
| Colaboracion real-time multi-usuario | Complejidad de sync | Versionado de archivos tradicional |
| Soporte Linux | Mercado minimo | Stack lo soporta, sin soporte oficial |
| Normativas fuera de Americas/Europa | Expansion futura | Arquitectura extensible para agregar |

Se mantiene el foco en el analisis; las funcionalidades de diseno estructural o de conexiones se abordaran en fases futuras (web/movil) para evitar retrasar el MVP y reducir riesgos legales.

### 3.3 Supuestos

1. OpenSees (con adaptadores para otros motores como Kratos) cubre los casos de analisis estructural del MVP y puede convivir con motores alternativos cuando el usuario lo requiera.
2. Hay demanda real en mercado Latam y Europa por una herramienta economica centrada en analisis con soporte NCh, AISC y Eurocodigos.
3. La precision del motor seleccionado debe alinearse con SAP2000, Robot y RISA para asegurar confianza profesional.
4. El desarrollo asistido por IA (Claude Code) acelera significativamente el trabajo y ayuda con la investigacion continua de competidores.
5. Los usuarios tienen acceso a internet para usar la plataforma cloud y sus funcionalidades colaborativas.

### 3.4 Dependencias Externas

| Dependencia | Tipo | Riesgo | Mitigacion |
|-------------|------|--------|------------|
| OpenSees Multiphysics | Motor calculo preferido | Medio (openseespy y versiones Python) | Versiones 3.11/3.12 probadas y adaptador robusto |
| Kratos Multiphysics | Motor alternativo | Bajo (BSD) | Adaptador modular disponible |
| Three.js | Visualizacion 3D | Bajo (MIT) | Ninguna |
| Python/FastAPI | Backend | Medio | Versiones LTS (3.11/3.12) alineadas con openseespy y dependencias |
| Normativas NCh/AISC/Euro | Documentacion | Medio | Acceso a normas oficiales y actualizacion continua |

---

## 4. Stakeholders

### 4.1 Stakeholders Internos

| Rol | Nombre | Necesidades | Responsabilidades | Nivel de Influencia |
|-----|--------|-------------|-------------------|---------------------|
| Ingeniero Estructural | Pablo | Precision de calculo, features de ingenieria, validacion tecnica | Define requisitos tecnicos, valida resultados, benchmark vs SAP2000 | Alto |
| Product Manager | Kevin | Arquitectura viable, plan ejecutable, producto comercializable | Decisiones tecnicas, gestion proyecto, arquitectura software | Alto |
| IA de Desarrollo | Claude | Documentacion clara, contexto estructurado, codigo mantenible | Implementacion de codigo, refactoring, testing | Medio |

### 4.2 Stakeholders Externos

| Rol | Perfil | Necesidades | Como Involucrarlo |
|-----|--------|-------------|-------------------|
| Usuario Early Adopter | Ingeniero independiente, 25-40 anos, Chile | Herramienta economica, facil de usar, resultados confiables | Beta testing, feedback directo |
| Usuario Oficina Pequena | Oficina 2-5 ingenieros, Latam | Licencias multiples economicas, soporte normativas locales | Piloto comercial |
| Usuario Estudiante | Estudiante ingenieria civil | Acceso gratuito/economico para aprender | Version educativa/freemium |
| Reguladores | Colegios de ingenieros | Software validado para proyectos oficiales | Certificacion de precision |

### 4.3 Matriz de Comunicacion

| Stakeholder | Frecuencia | Canal | Contenido |
|-------------|------------|-------|-----------|
| Pablo | Diaria | Reunion/Chat | Avances tecnicos, validaciones |
| Kevin | Diaria | Reunion/Chat | Decisiones, bloqueos, prioridades |
| Early Adopters | Semanal | Email/Video | Demos, feedback, bugs |
| Comunidad | Mensual | Blog/Redes | Actualizaciones, roadmap |

---

## 5. Restricciones

### 5.1 Restricciones Tecnicas

| ID | Restriccion | Impacto | Inamovible |
|----|-------------|---------|------------|
| RT-01 | Python 3.11+ backend obligatorio | Maximiza velocidad de desarrollo y evita conflictos con openseespy | Si |
| RT-02 | Cloud-first | Simplifica distribucion, requiere internet | Si |
| RT-03 | OpenSees preferido con motor intercambiable | Licencia abierta y adaptadores para otros motores garantizan flexibilidad | Si |
| RT-04 | React + Three.js frontend | Visualizacion 3D en browser | Si |
| RT-05 | Validacion vs SAP2000 / Robot / RISA | Credibilidad profesional | Si |

### 5.2 Restricciones de Recursos

| ID | Restriccion | Impacto | Mitigacion |
|----|-------------|---------|------------|
| RR-01 | Equipo pequeno (2 personas + IA) | Alcance limitado por iteracion | Priorizar MVP minimo, desarrollo asistido por IA |
| RR-02 | Presupuesto limitado | Sin cloud costoso, sin licencias caras | Servicios gratuitos/economicos, open source |
| RR-03 | Tiempo 6 meses MVP | Features reducidas inicialmente | Scope estricto, no feature creep |

### 5.3 Restricciones de Negocio

| ID | Restriccion | Impacto | Mitigacion |
|----|-------------|---------|------------|
| RN-01 | Precio competitivo (< 20% SAP2000) | Margen reducido | Volumen, costos bajos |
| RN-02 | Precision profesional obligatoria | Desarrollo cuidadoso, testing extensivo | Benchmark continuo vs SAP2000 |
| RN-03 | Soporte normativas Latam y europeas | Desarrollo especifico, documentacion normas | Priorizar NCh, AISC y Eurocodigos |

---

## 6. Criterios de Exito

### 6.1 Criterios de Exito del MVP

| Criterio | Metrica | Target | Metodo de Validacion |
|----------|---------|--------|----------------------|
| Funcionalidad core | Analisis estatico lineal completo | 100% casos base | Suite de tests automatizados |
| Precision | Correlacion con SAP2000 | >= 99% | Benchmark 10 modelos estandar |
| Rendimiento | Tiempo de calculo | <= 2x SAP2000 | Benchmark mismo hardware |
| Estabilidad | Crashes en uso normal | 0 en demo de 1 hora | Testing manual exhaustivo |
| Usabilidad | Workflow completo sin ayuda | Modelo -> Analisis -> Resultados | Testing con 3 usuarios externos |

### 6.2 Criterios de Exito del Producto (12 meses)

| Criterio | Metrica | Target | Metodo de Validacion |
|----------|---------|--------|----------------------|
| Adopcion | Usuarios activos mensuales | >= 100 | Analytics |
| Retencion | Usuarios que vuelven en 30 dias | >= 60% | Analytics |
| Satisfaccion | NPS | >= 40 | Encuesta usuarios |
| Comercial | Ingresos recurrentes | > $0 (validacion) | Ventas |
| Tecnico | Uptime sincronizacion | >= 99% | Monitoreo |

### 6.3 Criterios de Exito del Negocio (18 meses)

| Criterio | Metrica | Target | Metodo de Validacion |
|----------|---------|--------|----------------------|
| Product-Market Fit | Usuarios pagando | >= 20 | CRM |
| Expansion | Paises con usuarios | >= 3 | Analytics geografico |
| Sostenibilidad | Ingresos vs Costos | Break-even | Contabilidad |
| Reconocimiento | Mencion en comunidad ingenieria | >= 5 articulos/posts | Monitoreo medios |

---

## 7. Riesgos y Mitigaciones

### 7.1 Riesgos Tecnicos

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| OpenSees o adaptadores multi-motor no soportan algun tipo de analisis | Baja | Medio | Verificar capacidades temprano y mantener adaptadores para Kratos/RISA si es necesario |
| Three.js limitado para modelos grandes | Media | Medio | LOD, instancing, optimizacion WebGL |
| Latencia en analisis cloud | Baja | Bajo | Servidor con buena CPU, caching |
| Rendimiento insuficiente en modelos grandes | Media | Alto | Profiling temprano, optimizacion incremental |

### 7.2 Riesgos de Mercado

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Mercado Latam muy pequeno | Baja | Alto | Validar demanda con early adopters, pivotar si necesario |
| Competencia lanza version economica | Baja | Alto | Diferenciacion por normativas locales y UX |
| Usuarios no confian en software nuevo | Media | Medio | Benchmark publico, testimonios, version trial |

### 7.3 Riesgos de Ejecucion

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|--------------|---------|------------|
| Scope creep | Alta | Alto | Disciplina estricta, PRD detallado, backlog priorizado |
| Equipo muy pequeno | Media | Medio | IA development, priorizar, MVP minimo |
| Tiempo insuficiente | Media | Alto | Reducir scope MVP si necesario |

---

## 8. Roadmap de Alto Nivel

### Fase 1: MVP (Meses 1-2)
- Arquitectura cloud (FastAPI + React + Three.js)
- Motor de calculo OpenSees preferido con adaptadores multi-engine
- Modelacion basica (nodos, frames, grillas y Section Designer)
- Analisis estatico lineal con validacion contra SAP2000/Robot/RISA
- Visualizacion 3D web con overlay de resultados y grillas
- Importador de lineas AutoCAD y conversor rapido de unidades
- Auth + Pagos (Stripe)
- Deploy cloud

### Fase 2: V1.0 (Meses 3-6)
- Shells y elementos adicionales con grillas avanzadas y secciones mixtas
- Analisis dinamico, modos de vibrar y combinaciones normativas
- Librerias NCh y Eurocodigos completas con actualizacion AISC continua
- Mejoras de UX enfocadas en analisis y navegacion
- App movil basica centrada en analisis y conversion de unidades
- Piloto macOS + mejoras de interoperabilidad AutoCAD/SAP

### Fase 3: V2.0 (Meses 7-12)
- Analisis tiempo-historia, no lineal y chequeos multiengine
- Verificaciones normativas NCh/AISC/Euro completas
- Sincronizacion desktop-movil y pipeline de deployment
- Expansion regional con nuevas normativas y mercados en Latam/Europa
- Plan Enterprise

---

## 9. Decisiones Tecnicas

### 9.1 Decisiones Resueltas

| Decision | Resolucion | Justificacion |
|----------|------------|---------------|
| **Arquitectura** | Cloud-first (SaaS) | Sin instalacion, sin pirateria, cobro recurrente |
| **Motor calculo** | OpenSees preferido con adaptadores para Kratos u otros | OpenSees esta enfocado en estructuras y facilita alternar motores |
| **Backend** | Python 3.11+ + FastAPI | Versiones alineadas con openseespy mantienen rendimiento y compatibilidad |
| **Frontend** | React + Three.js | Visualizacion 3D en browser, multiplataforma |
| **Validacion** | vs SAP2000 / Robot / RISA | Multiples referencias industriales para generar confianza |
| **Pagos** | Stripe | Suscripciones automaticas |

### 9.2 Decisiones Pendientes

| Prioridad | Decision | Opciones | Deadline | Responsable |
|-----------|----------|----------|----------|-------------|
| **Media** | Sincronizacion cloud | Firebase, Supabase, Custom API | Antes de V2.0 | Kevin |
| **Media** | Framework movil | Flutter, React Native, Kivy | Antes de V2.0 | Kevin |
| **Media** | Modelo de negocio | Suscripcion, Licencia perpetua, Freemium | Antes de lanzamiento comercial | Kevin |
| **Baja** | Fuente datos AISC | Manual AISC, generacion desde formulas, open source | Durante F09 | Equipo |

---

## 10. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Ingeniero Estructural | Pablo | ______ | ______ |
| Product Manager | Kevin | ______ | ______ |

---

## 11. Pendientes Estrategicos

- Nombre del producto o modulo: "Nifes Forge" sigue en duda; evaluar alternativas como "Structural Forge" y definir si se lanza dentro o fuera de la marca Nifes.

## Anexos

### A. Documentos de Referencia
- INPUT.md: Transcripcion de planificacion original
- 0-analisis/requisitos.md: Requisitos funcionales y no funcionales
- 0-analisis/decisiones.md: Decisiones tecnicas
- 5-revision/revision.md: Revision cruzada de documentos

### B. Glosario
| Termino | Definicion |
|---------|------------|
| SAP2000 | Software de referencia de CSI (Computers and Structures Inc) |
| Kratos | Kratos Multiphysics - framework de simulacion open source (BSD license) |
| OpenSees | Framework de analisis estructural open source con openseespy para Python |
| Three.js | Libreria JavaScript para visualizacion 3D en browser |
| FastAPI | Framework Python para APIs de alto rendimiento |
| React | Framework JavaScript para interfaces de usuario |
| NCh | Norma Chilena |
| AISC | American Institute of Steel Construction |
| Frame | Elemento estructural lineal (viga, columna) |
| Shell | Elemento estructural de superficie (losa, muro) |
| Section | Propiedades geometricas y mecanicas de una seccion transversal |
| Engine | Motor de calculo (solver) para analisis estructural |

---

*Brief consolidado - Fase 6.0 DocGen*
*Proyecto PAZ - Software Profesional de Analisis Estructural*
