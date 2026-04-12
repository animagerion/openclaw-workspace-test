# La Realidad de la IA en Gestoras de Fondos: Lo que Nadie Te Cuenta

*Artículo para LinkedIn — Científico de Datos Senior, Gestora de Fondos Española*

---

La semana pasada circulaba un artículo sobre cómo los hedge funds usan IA. Listas de herramientas, screenshots de prompts, citas genéricas de "analistas". Todo muy ordenadito. Todo muy surface-level.

Después de trabajar años en data science aplicada a gestión de activos, voy a ser directo: ese tipo de contenido cuenta lo que pasa en la superficie y se salta todo lo difícil.

Vamos a ello.

---

## Los números que importan

Antes de hablar de ChatGPT, unos datos.

Según JPMorgan (2025), la adopción de IA en hedge funds pasó del 18% al 46% en un solo año. Un crecimiento del 156%. La AIMA confirma que el 95% de las gestoras dan acceso a múltiples herramientas de IA generativa a sus empleados. La inversión en datos alternativos supera ya los 1.000 millones de dólares anuales.

Parece que todo el mundo está en ello, ¿no?

El problema es que penetración no es igual a impacto. Y la diferencia la vas a encontrar en tres capas que nadie menciona.

---

## Capa 1: La capa de datos (donde se pierde el 80% del batalla)

El artículo que circulaba dedicaba exactamente cero líneas a lo más crítico: la calidad del dato.

En una gestora real, el dato es un desastre. Tienes sistemas legacy que llevan veinte años acumulando información en formatos incompatibles. Tienes datos de mercado que vienen de cinco proveedores distintos con metodologías distintas. Tienes datos internos — operaciones, flujos de clientes, posicionamiento — que están en hojas de cálculo controladas por personas que ya no están en la empresa.

Antes de que ningún modelo de lenguaje haga nada útil, alguien tiene que limpiar, estandarizar y enriquecer todo eso. Y eso no es sexy. No sale en los artículos.

**Lo que esto significa en la práctica:**

- El 60-70% del tiempo de un equipo de data science en una gestora se va en data engineering, no en modelado.
- Los datos más valiosos suelen ser los que nadie ha tocado nunca: logs de negociación, patrones de ejecución, datos alternativos externos.
- La diferencia entre una gestora que sacude IA sobre un data warehouse sucio y una que ha invertido en infraestructura de datos no se mide en meses, se mide en años.

El verdadero moat no es qué modelo usas. Es de qué datos dispones y cuánto trabajo ha costado dejarlos listos para usar.

---

## Capa 2: La integración con los procesos existentes

El artículo mencionaba que con IA puedes pasar de una semana de due diligence a horas. Técnicamente cierto. Operativamente, irrelevante sin contexto.

Porque en una gestora real, el proceso de inversión está lleno de checkpoints humanos, aprobaciones regulatorias, sistemas de cumplimiento, y departamentos enteros cuya existencia es precisamente ralentizar las cosas — para bien. No puedes inyectar IA en un proceso que depende de aprobaciones manuales sin rediseñar esas aprobaciones.

**Las preguntas que nadie hace en los artículos:**

- ¿Cómo se integra la salida de un modelo LLM en el sistema de gestión de riesgos de la firma?
- ¿Quién valida que la recomendación de IA es consistente con las restricciones regulatorias del fondo?
- ¿Qué pasa cuando el modelo dice una cosa y el gestor con veinte años de experiencia dice otra?

La respuesta más honesta es: depende de la madurez del proceso. Y la mayoría de gestoras españolas están en niveles muy tempranos de esa madurez.

---

## Capa 3: El talento y la cultura

Aquí es donde se caen la mayoría de iniciativas.

Necesitas personas que entiendan de modelos predictivos y también de mercados financieros. Ese perfil no existe. O mejor dicho: existe, pero cobra lo que pide y tiene ofertas de big tech, startups y fondos cuantitativos que pagan más.

Según el TIFF (Investment Fund Institute), uno de los principales impedimentos para la adopción de IA en gestoras es precisamente la dificultad para atraer talento especializado. El problema no es técnico. Es de mercado laboral.

Y luego está la cultura. Un gestor con veinte años de track record no va a cambiar su proceso porque una herramienta nueva le diga que está equivocado. Las decisiones de inversión son también decisiones políticas internas. Introducir IA en ese ecosistema requiere cambiar la dinámica de poder, no solo instalar software.

---

## El tema europeo: nuestro contexto importa

Casi todo lo que se publica sobre este tema viene de Estados Unidos. Y las gestoras europeas tenemos un contexto radicalmente diferente.

**MiFID II lo cambia todo.** La obligación de best execution, la documentación de decisiones de inversión, y los requisitos de reporting crean un entorno donde la explicabilidad no es opcional. No puedes tener un modelo de caja negra recomendando operaciones sin poder explicar por qué. Esto限制a qué tipo de modelos puedes desplegar y cómo.

**Los datos ESG son un campo de batalla diferente.** Mientras en Estados Unidos el debate ESG es político, en Europa es regulatorio. Tienes que reportar métricas de sostenibilidad que requieren datos que muchas veces no existen o son de fuentes no comparables. Aquí la IA puede ayudar a conectar datos dispersos, estimar variables que no se publican, y crear scores propietarios. Es un área donde quien llegue primero tiene ventaja real.

**La estructura del mercado es distinta.** Menos fondos cuantitativos pure-play que en USA, más gestión discrecional, mayor peso de la banca privada y los fondos de pensiones. Esto significa que los casos de uso más relevantes para nuestro mercado no son los del artículo de turno sobre hedge funds.

---

## Lo que sí funciona ahora mismo

Después de todo lo anterior, sé que puede parecer que soy pesimista. No lo soy. Solo soy preciso.

Lo que sí funciona hoy con impacto medible:

1. **Procesamiento de información no estructurada.** Transcripciones de earnings calls, informes de research, noticias. Aquí los LLMs dan un salto real en velocidad. No descubres alfa, pero procesas más fondo más rápido.

2. **Asistencia en modelos cuantitativos.** No para reemplazar al modelo, sino para limpiar datos, hacer primer análisis exploratorio, detectar anomalías. Como un analista junior que trabaja a velocidad máquina.

3. **Automatización de compliance y reporting.** Aquí el ROI es claro y rápido. Revisar que las operaciones cumplen con las restricciones del fondo, generar informes regulatorios, detectar posibles conflictos de interés. Tareas de alto volumen y baja ambigüedad.

4. **Análisis de sentimiento estructurado.** No para generar señales de trading directamente, sino para alimentar modelos cuantitativos con features derivadas de sentimiento de mercado.

---

## Un punto honesto sobre lo que no funciona

No funciona — todavía —:

- Reemplazar el juicio del gestor en decisiones de asignación strategic.
- Generar alpha directamente desde prompts genéricos.
- Predicción de tendencias macro a partir de datos públicos.
- Ningún modelo, por bueno que sea, que trabaje sobre datos de calidad baja.

El artículo que mencionaba al principio fracasaba en exactamente esto: presentaba la IA como una herramienta mágica que se conecta al proceso existente y mejora todo. La realidad es que solo mejora las partes del proceso que ya estaban bien diseñadas. Si el proceso es débil, la IA lo hace débil más rápido.

---

## ¿Qué deberían hacer las gestoras ahora?

Si tuviera que resumirlo en acciones concretas:

**Corto plazo (0-12 meses):**
- Identificar 2-3 procesos de alto volumen y baja ambigüedad donde la IA generativa puede aportar eficiencia inmediata. Compliance y reporting son los candidatos obvios.
- No comprar más herramientas. Mejorar la calidad del dato existente. Cada euro en data engineering rinde más que cada euro en licencias de IA.

**Medio plazo (1-3 años):**
- Construir capacidades internas de ML aplicado, no de investigación. El objetivo no es publicar papers; es resolver problemas concretos de negocio.
- Empezar a experimentar con datos alternativos donde la competencia es menor: datos de sostenibilidad, datos de posicionamiento de mercado, datos de flujo.

**Largo plazo:**
- Integrar IA en el proceso de inversión no como herramienta isolated, sino como parte de una rediseño del proceso. Esto requiere que los equipos de inversión lideren, no los de tecnología.

---

## El punto que me importa destacar

No escribo esto para desanimar. Escribo esto porque el entusiasmo mal dirigido es peligroso.

He visto gestoras gastar millones en plataformas de IA que no mejoran nada porque el problema real — datos malos, procesos rotos, cultura closed — no se tocó. Y he visto equipos pequeños hacer más con modelos sencillos y datos limpios que fondos enormes con presupuestos de IA desproporcionados.

La IA no va a transformar la gestión de activos por arte de magia. Va a transformar a las gestoras que se molesten en entender dónde está su problema real y tengan la disciplina de resolverlo antes de comprar la siguiente herramienta.

Que no te vendan la transformación. Exige el diagnóstico primero.

---

*¿Trabajas en data science para una gestora y quieres compartir perspectiva? Me interesa conocer qué casos de uso estáis viendo en el mercado español. Conectamos.*
