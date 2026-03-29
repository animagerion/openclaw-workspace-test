# Tutor Educativo con OpenClaw para estudiante de 13 años (España)

**Proyecto:** Agente tutor AI personalizado  
**Autor:** Investigación Gerion  
**Fecha:** 29 de marzo de 2026  
**Destinatario:** Paduel (padre)  

---

## Resumen ejecutivo

Paduel quiere un tutor AI para su hijo de 13 años (2º-3º ESO) que mejore sus resultados académicos en el sistema educativo español y permita aprender más allá del currículo. OpenClaw ya está configurado como agente personal.

**Conclusión principal:** Existe un hueco de mercado claro para un tutor AI que conozca específicamente el currículo LOMLOE español, sea personalizable al nivel del alumno, cubra tanto refuerzo como ampliación, y respete la privacidad de menores. La combinación de OpenClaw + prompts especializados + APIs de generación de contenido es viable como MVP.

**Dato clave de privacidad:** Con la legislación española en evolución (anteproyecto de ley 2024 eleva a 16 años la edad de consentimiento digital), cualquier solución debe tener consentimiento parental verificable y cumplir RGPD pediátrico.

---

## 1. Estado del arte: Herramientas existentes

### 1.1 Herramientas internacionales de tutoring AI

#### Khanmigo (Khan Academy)
- **Qué es:** Tutor AI basado en GPT-4, built on top of Khan Academy
- **Precio:** $4/mes (individual) / $9/mes (familias)
- **Método:** Socrático — nunca da respuestas directas, guía con preguntas
- **Calificación:** 4/5 estrellas (Common Sense Media) — una de las mejor valoradas
- **Fortalezas:**
  - Contenido curricular extenso y bien estructurado
  - Diseñado responsablemente para educación (marcos NIST, AI Ethical Framework)
  - Actividades多样性: debates, co-escritura, juegos de palabras
  - Para profesores: genera planes de lección, rúbricas, preguntas de salida
- **Limitaciones:**
  - Basado en curriculum estadounidense, NO alineado con LOMLOE
  - Dificultades con matemáticas avanzadas (los LLM "predicen" texto, no razonan)
  - Sin input visual (no acepta fotos de problemas)
  - En inglés (o muy limitado en español)
- **Adecuación para el caso:** Parcial. Muy bueno como referencia metodológica pero no sirve directamente para un estudiante español.

#### Duolingo
- **Qué es:** App de aprendizaje de idiomas con IA adaptativa
- **Precio:** Gratis (con límites) / ~€7/mes Super
- **Fortalezas:** Gamificación efectiva, ejercicios cortos, feedback inmediato
- **Limitaciones:** Enfoque en idiomas únicamente, metodología de app móvil (no tutoría profunda), menos efectivo para inglés de examen Cambridge
- **Adecuación:** Útil como complemento para aprender idiomas pero insuficiente como tutor general.

#### Photomath / Mathway
- **Qué es:** Resolvedores de problemas matemáticos con pasos
- **Precio:** Photomath gratis / ~€10/mes Premium; Mathway ~€10/mes
- **Fortalezas:**
  - Reconocimiento de fotos de problemas (Photomath)
  - Paso a paso detallado
  - Cubre desde aritmética básica hasta cálculo
- **Limitaciones críticas:**
  - Dan la solución directamente — fomentan copiar, no aprender
  - NO explican el "por qué", solo el "cómo"
  - Sin personalización ni seguimiento del progreso
  - Ajenos al currículo español (usan terminología y estructura anglosajona)
- **Adecuación:** Peligroso como herramienta única para un estudiante de 13 años. Útil como "segunda opinión" bajo supervisión.

#### Wolfram Alpha Pro
- **Qué es:** Motor de conocimiento computacional con soluciones paso a paso
- **Precio:** ~$7/mes para estudiantes (descuento educativo)
- **Fortalezas:** Exacto en matemáticas, ciencias, datos reales. Step-by-step en Pro.
- **Limitaciones:**
  - Curva de aprendizaje alta — no es intuitivo para un estudiante de 13 años
  - Sin guías pedagógicas, solo respuestas
  - Caro si se quiere para toda la familia
  - En inglés
- **Adecuación:** Mejor para estudiantes mayores o especializados en ciencias.

#### ChatGPT / Claude / Gemini (uso genérico)
- **Qué son:** LLMs generalistas
- **Precio:** ChatGPT gratis / Plus $20/mes; Claude gratis / Pro $20/mes; Gemini gratis / Ultra $20/mes
- **Fortalezas:** Versatilidad total, explican cualquier tema
- **Limitaciones críticas:**
  - NO conocen el currículo español
  - Pueden inventar información ("alucinaciones") — especialmente peligroso en matemáticas y ciencias
  - Sin estructura pedagógica ni seguimiento
  - Privacidad dudosa para menores (términos de servicio pensados para adultos)
  - Pueden dar respuestas incorrectas que un estudiante no sabe identificar como tales
- **Adecuación:** Potente como herramienta complementaria SI se sabe usar, pero NO es un tutor seguro para un menor sin supervisión.

### 1.2 Plataformas educativas en España

#### Smartick
- **Qué es:** Método online de aprendizaje personalizado para niños 4-14 años
- **Precio:** ~€20-25/mes (depende del plan)
- **Fortalezas:**
  - Empresa española
  - Sesiones de 15 minutos/día — adaptéame al ritmo del niño
  - Matemáticas + lectura + programación + pensamiento crítico
  - 94% de alumnos mejoran capacidades matemáticas (estudio piloto 33 colegios Madrid)
  - 70% mejora su nota
  - "Engancha" según usuarios — gamificación efectiva
- **Limitaciones:**
  - Diseñado para niños más pequeños (hasta 14 años, pero muy enfocado a primaria/principio ESO)
  - NO cubre todas las materias de la ESO — énfasis en matemáticas
  - Metodología de "sesiones cortas diarias" — puede quedarse corto para un estudiante de 13 años que necesita profundizar
  - Sin tutor conversacional — ejercicios adaptativos, no diálogo
- **Adecuación:** Muy bueno para matemáticas de 2º-3º ESO como complemento, pero no cubre el resto de asignaturas ni funciona como tutor general.

#### Tututor AI (tututor.ai)
- **Qué es:** Plataforma española de IA para docentes y estudiantes
- **Precio:** Planes desde ~€4.95/mes (individuals) — verificado en web
- **Fortalezas:**
  - Alineado con el currículo español (LOMLOE)
  - Crea situaciones de aprendizaje, unidades didácticas, exámenes y rúbricas
  - En español
  - Para docentes principalmente, pero con tutoría para estudiantes
- **Limitaciones:**
  - Enfoque más hacia profesores que hacia estudiantes individuales
  - No es un agente conversacional personalizado
- **Adecuación:** Interesante como referencia para materiales, pero no como tutor personalizado.

#### Educaixa / Kahoot / Cerebriti / ClassDojo
- **Qué son:** Plataformas de gamificación y recursos educativos
- **Fortalezas:** Amplio uso en colegios españoles, contenido alineado con currículo
- **Limitaciones:** Son herramientas de creación de actividades/trivial, no tutores AI
- **Adecuación:** Útiles como complemento para practicar pero no como tutoring personal.

#### Repositorios institucionales (INTEF, EducaMadrid, Cide@, Procomún, Agrega)
- **Qué son:** Bancos de recursos educativos públicos y gratuitos
- **Fortalezas:** Contenido de calidad, alineado con currículo, gratis
- **Limitaciones:** NO son herramientas AI, son repositorios de materiales estáticos
- **Adecuación:** Buenos como fuente de referencia, no como tutor.

### 1.3 Tabla comparativa resumida

| Herramienta | Curriculum español | Tutor conversacional | Personalizado | Privacidad menores | Precio aprox. | Apto 13 años |
|---|---|---|---|---|---|---|
| Khanmigo | ✗ (US) | ✓ | ✓ | ✓ | $4/mes | ✓ (pero en inglés) |
| Smartick | ✓ (ES) | ✗ | ✓ | ✓ | €20-25/mes | ✓ (limitado a mates) |
| Tututor AI | ✓ | ✗ | Parcial | ✓ | €5/mes | ✓ |
| Megaprofe | ✓ | ✗ | Parcial | ✓ | €5/mes | ✓ (docentes) |
| Photomath | ✗ | ✗ | ✗ | ✗ | Gratis/€10 | ⚠️ (dar soluciones) |
| ChatGPT/Claude | ✗ | ✓ | ✗ | ✗ | Gratis/$20 | ⚠️ (sin filtro) |
| Wolfram Alpha | ✗ | ✗ | ✗ | ✗ | $7/mes | ⚠️ (complejo) |

**Conclusión del estado del arte:** NO existe actualmente una herramienta que combine: tutor conversacional AI + alineación total con currículo LOMLOE + personalización al nivel del estudiante + privacidad para menores + cubra múltiples materias + permita ir más allá del currículo.

---

## 2. Análisis del currículo LOMLOE para 2º-3º ESO (13 años)

### 2º ESO (más común para 13 años)

#### Matemáticas
- **Números:** Divisibilidad, múltiplos, divisores, primos, operaciones con enteros, potencias, raíces
- **Decimales y sexagesimal:** Sistema decimal, operaciones con decimales, sistema sexagesimal (tiempo/ángulos)
- **Fracciones:** Equivalencia, operaciones, problemas aritméticos
- **Proporcionalidad:** Directa, inversa, porcentajes, aumentos/disminuciones porcentuales
- **Álgebra:** Expresiones algebraicas, monomios, polinomios, extracción de factor común
- **Ecuaciones:** Ecuaciones de primer grado, sistemas de ecuaciones (sustitución), problemas con ecuaciones
- **Geometría:** Teorema de Pitágoras, figuras semblantes, cuerpos geométricos (prismas, pirámides, cilindros, conos, esferas)
- **Funciones:** Concepto de función, crecimiento/decrecimiento, funciones lineales y=mx+n
- **Estadística y probabilidad:** Población, muestra, tablas de frecuencias, diagramas, parámetros de centralización

#### Lengua Castellana y Literatura
- Comprensión lectora y expresión escrita
- Gramática: sintagma nominal y verbal, análisis morfológico básico
- Ortografía avanzada
- Comentario de texto
- Historia de la literatura española (autores y obras clave)
- Tipos de texto: narrativo, descriptivo, argumentativo

#### Ciencias Naturales
- Biología: célula, nutrición, reproducción, ecosistemas
- Geología básica: minerales, rocas, estructura terrestre
- Salud y cuerpo humano (detalle varía según comunidad)

#### Geografía e Historia
- Historia: Edad Media, Edad Moderna (hasta el siglo XVII)
- Geografía física y humana de Europa y España
- Organización política y territorial de España

#### Inglés (enfoque B1 Preliminary/Cambridge)
- Destrezas: Reading, Writing, Listening, Speaking
- Gramática: Present perfect, past simple/continuous, used to, comparativos, condicionales básicos
- Vocabulario: Situaciones comunicativas del nivel B1
- Ejercicios tipo examen Cambridge PET

#### Segunda lengua extranjera (Francés o Alemán, según centro)
- Nivel básico A1-A2
- Francés: Pronunciación, saludo, familia, ocio, presente de indicativo
- Alemán: Bases fonéticas, artículos, presente de verbos regulares

#### Tecnología y Programación
- Introducción a la programación (Scratch, Python básico en algunos centros)
- Ofimática básica
- Proyecto técnico (diseño y construcción)

#### Educación Plástica, Visual y Audiovisual
- Dibujo técnico básico (líneas, ángulos, figuras)
- Color y composición
- Expresión artística

#### Música
- Lenguaje musical: notas, escalas, ritmo
- Práctica instrumental (flauta dulce u otro instrumento)
- Audiciones y análisis de obras

#### Religión / Valores Éticos
- Según elección familiar

### 3º ESO (algunos estudiantes de 13 años están en 3º)

Similar a 2º pero introduce:
- **Física y Química** (nueva asignatura): Leyes de Newton, energía, cinemática básica, cambios químicos, tabla periódica, reacciones químicas
- **Álgebra más avanzada:** Ecuaciones de segundo grado
- **Funciones más complejas:** Funciones cuadráticas
- **Biología más profunda:** Genética básica, evolución

**Implicación para el tutor:** El rango de 2º-3º ESO cubre muchas materias pero con temáticas muy concretas y identificables. Un tutor que conozca estos temas específicos será mucho más útil que un chatbot genérico.

---

## 3. Evaluación de idoneidad de herramientas existentes

### Criterios utilizados
- **Edad:** ¿Apropiado para 13 años?
- **Curriculum:** ¿Alineado con LOMLOE?
- **Personalización:** ¿Se adapta al nivel del alumno?
- **Más allá del currículo:** ¿Permite ampliación?
- **Privacidad:** ¿Cumple RGPD para menores?
- **Coste:** ¿Asequible?
- **Qué SÍ puede hacer vs qué NO**

### Evaluaciones individuales

#### Khanmigo
- **Edad:** ✓
- **Curriculum:** ✗ (US)
- **Personalización:** ✓
- **Más allá:** ✓
- **Privacidad:** ✓ (diseñado para menores, sin venta de datos)
- **Coste:** $4/mes = ~€3.5/mes — accesible
- **SÍ:** Tutor conversacional, guías socráticas, múltiples materias
- **NO:** No está en español, no conoce currículo español, limitado en mates

#### Smartick
- **Edad:** ✓ (4-14)
- **Curriculum:** ✓ (español)
- **Personalización:** ✓
- **Más allá:** Parcial (puede avanzar rápido)
- **Privacidad:** ✓ (empresa española, RGPD)
- **Coste:** €20-25/mes — moderado-alto
- **SÍ:** Maths ultra-adaptativo, sessions cortas, resultados medibles
- **NO:** Solo matemáticas, no tutoría conversacional, no otras asignaturas

#### Photomath
- **Edad:** ⚠️ (puede facilitar copiar)
- **Curriculum:** ✗ (terminología anglosajona)
- **Personalización:** ✗
- **Más allá:** ✗
- **Privacidad:** ⚠️ (recolecta datos de uso)
- **Coste:** Gratis/€10/mes
- **SÍ:** Resuelve problemas con pasos, puede ayudar a entender
- **NO:** Fomenta dependencia, alucinaciones en problemas complejos, sin contexto pedagógico

#### ChatGPT/Claude
- **Edad:** ⚠️ (sin filtros específicos para menores)
- **Curriculum:** ✗ (no conoce LOMLOE específicamente)
- **Personalización:** Parcial (puede recordar contexto en una sesión)
- **Más allá:** ✓✓✓
- **Privacidad:** ✗ (no diseñado para menores)
- **Coste:** Gratis o $20/mes
- **SÍ:** Explica cualquier tema, versatile, ayuda con写作
- **NO:** Alucina en mates/ciencias, puede dar información incorrecta sin avisar, sin seguimiento pedagógico

#### Wolfram Alpha Pro
- **Edad:** ⚠️ (complejo para 13 años)
- **Curriculum:** ✗ (US)
- **Personalización:** ✗
- **Más allá:** ✓
- **Privacidad:** Parcial
- **Coste:** $7/mes — aceptable
- **SÍ:** Exactitud en matemáticas y ciencias, step-by-step
- **NO:** Curva de aprendizaje alta, interfaz no amigable, no pedagógico

---

## 4. Oportunidades identificadas (huecos de mercado)

### 4.1 Lo que nadie cubre bien

1. **Tutor AI conversacional en español que conozca LOMLOE**
   Nadie ofrece un chatbot que realmente sepa qué se imparte en 2º de ESO en España, con qué nivel de detalle, qué tipo de ejercicios entran en examen.

2. **Generador de ejercicios personalizados con dificultad progresiva**
   Los sistemas existentes o dan soluciones (Photomath) o son genéricos (ChatGPT). Falta un sistema que entienda qué sabe el alumno y genere ejercicios exactamente a su nivel.

3. **Tutor de inglés B1 Cambridge para adolescentes**
   Hay apps para inglés general (Duolingo) pero nada específico que prepare para el PET Cambridge con metodología de examen y práctica real de las 4 destrezas.

4. **Coach de estudio personalizado para secundaria**
   No existe una herramienta que enseñe técnicas de estudio (Pomodoro, mapas mentales, schedules) adaptadas a un estudiante español de 13 años con sus materias específicas.

5. **Preparación estructurada para exámenes trimestrales**
   Un sistema que pueda generar simulacros de examen tipo "test de autoevaluación" para cada materia y trimestre.

6. **Recuperación de temas suspensos**
   Un asistente que detecte qué temas tiene pendientes y cree un plan de recuperación progresivo.

7. **Tutor de programación para la asignatura de Tecnología**
   Python básico, Scratch, o Arduino — con ejercicios progresivos y proyectos.

8. **Generador de resúmenes y fichas de estudio**
   Que parta del temario real de cada materia y genere fichas tipo "apuntes visuales" o "resumen de una cara" para estudio.

---

## 5. Concepto de Tutor Ideal

### ¿Qué hace realmente útil a este tutor vs un chatbot genérico?

El diferenciador fundamental es la **profundidad de contexto educativo específico**:

**El tutor debe:**

1. **Conocer el currículo LOMLOE** — Saber que en 2º ESO el tema de ecuaciones incluye ecuaciones de primer grado con denominadores, no solo x+3=5. Saber la diferencia entre Maths de 2º y 3º ESO.

2. **Tener sentido de progreso académico real** — Saber que el alumno va bien en proporcionalidad pero flojea en operaciones con enteros. Mantener un perfil de fortalezas/debilidades por materia.

3. **Hablar "la lengua del examen"** — Conocer qué tipo de preguntas entran en los exámenes trimestrales españoles, cómo se pide en la Selectividad/EvAU (para 4º ESO y Bachillerato), y preparar con esa meta en mente.

4. **Generar contenido específico y verificable** — No respuestas genéricas de Wikipedia, sino ejercicios y explicaciones adaptados al temario español real.

5. **Ser un complemento, no un sustituto** — Fomentar el pensamiento crítico, no dar las respuestas directamente (método Socrático inspirado en Khanmigo).

6. **Responder en el contexto del libro de texto** — "En la página 72 de tu libro de Santillana, el ejercicio 5 de ecuaciones..." (si se integra con PDFs de libros).

7. **Incluir coaching de estudio** — No solo académica la tutoría; también enseñar a organizarse, a hacer resúmenes, a preparar exámenes.

---

## 6. Ideas priorizadas

### Idea 1: Tutor LOMLOE Conversacional (PRIORIDAD ALTA — MVP)

**Descripción:** Agente conversacional especializado en el currículo de 2º-3º ESO español. Conoce tema por tema qué se imparte en cada materia, puede explicar conceptos, generar ejercicios a medida, y detectar lagunas.

**Cómo funciona:**
- Paduel o el estudiante indica la materia y tema específico
- El tutor explica con ejemplos, adapta el nivel
- Genera ejercicios con soluciones explicadas paso a paso
- Si el alumno falla, detecta el hueco y propone refuerzo

**Diferenciación:** Es Khanmigo pero en español y con currículo español.

**Coste técnico:** Requiere un LLM (MiniMax o GPT-4o mini vía API) + base de conocimiento con temario LOMLOE. Integrable en OpenClaw.

---

### Idea 2: Generador de Exámenes y Simulacros (PRIORIDAD ALTA)

**Descripción:** El tutor puede generar exámenes de prueba tipo test o problemas para cualquier tema de cualquier materia, con dificultad calibrable. Incluye soluciones completas.

**Cómo funciona:**
- "Genera un examen de 10 preguntas de ecuaciones de primer grado para 2º ESO, nivel medio"
- El tutor crea el examen en formato texto/markdown
- También puede crear "exámenes tipo trimestral" con mezcla de temas
- Genera la solución para que el estudiante se autocorrija

**Diferenciación:** Photomath da soluciones; esto genera problemas nuevos calibrados.

**Aplicación directa:** El estudiante puede practicar antes de exámenes reales.

---

### Idea 3: Preparador B1 Cambridge (PRIORIDAD MEDIA-ALTA)

**Descripción:** Tutor especializado en el examen Cambridge B1 Preliminary (PET). Practica las 4 destrezas (Reading, Writing, Listening, Speaking) con ejercicios tipo examen y feedback.

**Cómo funciona:**
- Práctica deReading: ejercicios de comprensión lectora nivel PET
- Writing: prácticas de redacciones tipo examen con feedback
- Listening: ejercicios con audios (usando recursos disponibles)
- Speaking: guía de estructuras y práctica de temas frecuentes
- Mock tests completos con temporización

**Diferenciación:** Duolingo no prepara específicamente para Cambridge. Los cursos de academia son caros (€15-25/hora).

**Coste:** Solo el tiempo de crear prompts especializados + acceso a materiales de práctica.

---

### Idea 4: Coach de Estudio y Organización (PRIORIDAD MEDIA)

**Descripción:** El tutor no solo ayuda con contenido académico sino con CÓMO estudiar. Técnicas de estudio adaptadas a la ESO española.

**Cómo funciona:**
- Planificador de estudio semanal por materias
- Técnica Pomodoro integrada
- Guía para hacer resúmenes y mapas mentales
- Consejos para preparar exámenes (qué repetir, cómo hacer схемы)
- Check-ins de progreso

**Diferenciación:** Herramientas como Notion o Trello existen pero no están pensadas para un estudiante de 13 años con currículo español específico.

**Beneficio colateral:** Reduce la sobrecarga del estudiante, algo muy común en ESO.

---

### Idea 5: Tutor de Programación Python/Scratch (PRIORIDAD MEDIA)

**Descripción:** Para la asignatura de Tecnología, el tutor guía al estudiante en programación con Python o Scratch, explicando conceptos paso a paso y generando proyectos alineados con el currículo.

**Cómo funciona:**
- Lecciones interactivas de Python básico (variables, bucles, condicionales, funciones)
- Proyectos graduados: desde un juego simple en Scratch hasta un programa en Python
- Ayuda con ejercicios de tecnología
- Proyecto final por trimestre

**Diferenciación:** No hay herramientas que preparen específicamente para la parte de programación de Tecnología 2º-3º ESO.

---

## 7. Plan de actuación

### Fase 1: MVP (Semanas 1-4)
**Objetivo:** Tutor LOMLOE conversacional básico funcional

- Crear un conjunto de system prompts especializados para cada materia de 2º-3º ESO
- Probar con OpenClaw existente (MiniMax como LLM)
- Centrarse en 2-3 materias prioritarias: Matemáticas, Lengua, Inglés
- Documentar qué funciona y qué no

**Entregable:** El estudiante puede mantener una conversación sobre cualquier tema de estas materias y recibir explicaciones + ejercicios adaptados.

**Coste:** Solo tiempo de creación de prompts. APIs de OpenClaw ya pagadas.

---

### Fase 2: Generador de Ejercicios y Exámenes (Semanas 5-8)

- Añadir capacidad de generar ejercicios estructurados
- Crear templates de examen para cada materia
- Implementar sistema simple de seguimiento (por archivo JSON/markdown)
- Extender a más materias: Física/Química (3º), Geografía, Historia

**Entregable:** "Genera un examen de 10 preguntas de funciones lineales para 2º ESO" funciona perfectamente.

---

### Fase 3: B1 Cambridge + Coach de Estudio (Semanas 9-12)

- Módulo de preparación Cambridge B1
- Guía de técnicas de estudio + planificador semanal
- Sistema de seguimiento de progreso por materia

**Entregable:** El estudiante tiene una herramienta de estudio completa semanal.

---

### Fase 4: Expansión y Refinamiento (Mes 4+)

- Integración con libros de texto (subir PDF y preguntar por página)
- Tutor de programación
- Tutor de segunda lengua (francés/alemán)
- Alumno puede subir sus exámenes y recibir análisis de errores

---

## 8. Consideraciones técnicas

### Stack tecnológico
- **OpenClaw** ya instalado y funcionando — es la base
- **LLM:** MiniMax (ya disponible) o GPT-4o mini (OpenAI) para mejor rendimiento
- **Almacenamiento:** Sistema de archivos local para perfil del alumno, historial de sesiones, ejercicios generados
- **APIs externas opcionales:**
  - Wikipedia API (para consultas factuales)
  - Wolfram Alpha API (para verificaciones matemáticas exactas)
  - Kahoot API (para gamificación — no crítico)

### Coste estimado
- **Fase MVP:** €0 (usa OpenClaw existente)
- **Fase 2+:** Coste API adicional si se usa OpenAI: ~$5-20/mes para uso moderado
- **Infraestructura:** €0 (todo en local, nada en la nube)

### Integración con OpenClaw
La clave es crear **skills especializados** de OpenClaw para cada módulo:
- Skill `tutor-eso-mates`: Matemáticas 2º-3º ESO
- Skill `tutor-eso-lengua`: Lengua Castellana
- Skill `tutor-eso-ingles`: Inglés B1 Cambridge
- Skill `tutor-eso-ciencias`: Ciencias (Naturales, FyQ)
- Skill `tutor-examenes`: Generador de exámenes
- Skill `tutor-coach`: Coaching de estudio

### Privacidad y RGPD (CRÍTICO)
- **Menores de 13 años:** RGPD establece que el tratamiento de datos de menores requiere consentimiento parental para menores de 16 años (España, con proyecto de ley 2024/16 años).
- **Recomendaciones:**
  - Consentimiento parental documentado (aunque OpenClaw sea uso familiar)
  - NO enviar datos del estudiante a APIs externas sin control
  - Preferir LLM que corra localmente o en proveedores con política clara de no retención de datos
  - OpenClaw con MiniMax (proveedor chino con política de no retención para ряask): verificar
  - No almacenar datos sensibles del menor más allá del contexto de sesión
  - Si se usa OpenAI: verificar que no entrenan con datos del usuario (política actual: no entrenan con datos de API)

---

## 9. Riesgos y limitaciones

### Riesgos principales

1. **Alucinaciones en mates/ciencias**
   Los LLM pueden dar soluciones incorrectas en matemáticas. Mitigación: Verificar ejercicios de matemáticas con Wolfram Alpha o doble check manual. Usar método Socrático (preguntas guía) en vez de dar la respuesta directa.

2. **Dependencia del estudiante**
   Si el tutor es demasiado útil, el estudiante puede depender de él para todo. Mitigación: Diseñar interacciones que siempre requieran esfuerzo del estudiante ("¿Cómo empezarías tú?" en vez de "La solución es...").

3. **Privacidad de menores**
   La legislación española está endureciendo los requisitos para menores en entornos digitales. Riesgo alto si no se gestiona correctamente. Mitigación: Consentimiento parental, datos en local, mínimo procesamiento externo.

4. **Desactualización del currículo**
   Las comunidades autónomas adaptan el currículo LOMLOE de forma ligeramente diferente. Mitigación: El tutor debe indicar la comunidad autónoma y centrarse en contenidos comunes a todo España (que son la mayoría).

5. **Coste de APIs**
   Si el uso crece, el coste de APIs puede aumentar. Mitigación: Empezar con MiniMax (coste bajo), monitorizar uso.

### Limitaciones conocidas

- **No puede reemplazar a un professor/tutor humano:** Un LLM no puede detectar matices emocionales, motivación profunda, o problemas de aprendizaje específicos (TDAH, dislexia, etc.)
- **No tiene acceso a los libros de texto específicos** hasta que se integren (PDFs)
- **No puede corregir exámenes de forma automática** a menos que sean de texto/simple
- **No puede reemplazar la práctica social** de idiomas ( Speaking requiere interlocutores reales)

---

## 10. Anexos

### Contenido matemático detallado 2º ESO
(Referencia para construir prompts del tutor)

```
BLOQUE 1: NÚMEROS Y ÁLGEBRA
- Divisibilidad: múltiplos, divisores, primos, factorization
- Números enteros: operaciones combinadas, potencias, raíces
- Fracciones: equivalencia, operaciones, problemas
- Proporcionalidad: directa, inversa, porcentajes
- Álgebra: expresiones algebraicas, monomios, polinomios
- Ecuaciones: 1er grado (con denominadores), sistemas (sustitución)
- Problemas con ecuaciones

BLOQUE 2: GEOMETRÍA
- Teorema de Pitágoras (catetos, hipotenusa)
- Semejanza de triángulos
- Cuerpos geométricos: prismas, pirámides, cilindros, conos, esferas
- Volúmenes

BLOQUE 3: FUNCIONES
- Concepto de función
- Funciones lineales: y=mx+n
- Funciones constantes: y=k
- Crecimiento/decrecimiento, máximos/mínimos

BLOQUE 4: ESTADÍSTICA
- Población, muestra, variables
- Tablas de frecuencias
- Diagramas de barras, sectores, histogramas
- Parámetros: media, mediana, moda
- Probabilidad básica
```

### Recursos de referencia para construir el tutor

- **Currículo oficial LOMLOE:** https://educagob.educacionfpydeportes.gob.es/curriculo/curriculo-lomloe/menu-curriculos-basicos/ed-secundaria-obligatoria.html
- **Real Decreto 217/2022 (curriculum mínimo nacional):** BOE-A-2022-4975
- **Cambridge B1 Preliminary formato:** https://www.cambridgeenglish.org/es/exams-and-tests/preliminary-for-schools/exam-format/
- **INTEF (recursos educativos):** https://intef.es/
- **AEPD guía menores:** https://www.aepd.es/guias/estrategia-menores-aepd-lineas-accion.pdf

---

*Documento preparado como base para el desarrollo del proyecto. Requiere validación con el estudiante real (materias donde más necesita ayuda, ritmo de uso, preferencias) para afinar las prioridades.*
