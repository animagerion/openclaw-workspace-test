# AskB: el asistente de IA que está transformando el terminal de Bloomberg

Llevo años trabajando con el terminal de Bloomberg. Es el estándar de la industria financiera: datos en tiempo real, cobertura global, profundidad de información inigualable. Pero también es conocido por tener una curva de aprendizaje brutal y una interfaz que, siendo amable, no se diseñó pensando en la accesibilidad.

Cuando salió AskB —el módulo de IA conversacional de Bloomberg integrado en el terminal y accesible vía Terminal Anywhere— lo primero que pensé fue: "Otra capa sobre un sistema ya complejo". Después de unos meses usándolo de forma regular, mi opinión ha cambiado. Y no de la forma que esperaba.

## Qué es AskB

AskB es un interfaz de IA conversacional que permite consultar datos del terminal usando lenguaje natural. En lugar de memorizar fórmulas, saber navegar menús o construir tablas desde cero, puedes simplemente preguntar: "Dame la yield del bono español a 10 años" o "Compáreme el PER del sector utilities en Europa vs. EE.UU. los últimos 5 años".

Está integrado directamente en el terminal clásico, pero también accesible desde Terminal Anywhere — el acceso basado en navegador que te permite conectar al terminal sin instalación de software. Esto último es clave.

## Lo que funciona bien

**Velocidad.** La respuesta es casi instantánea. No estás esperando a que el modelo procese nada pesado — AskB traduce tu pregunta a queries que el terminal ya sabe resolver. Es como tener un traductor entre tu idioma y el del sistema.

**Acceso remoto.** Poder consultar datos de Bloomberg desde casa, desde el móvil, o desde cualquier sitio sin VPN ni instalación pesada cambia las cosas. Para alguien que trabaja en remoto como yo, esto no es un extra — es prácticamente una necesidad.

**Rango de consultas.** Preguntas straightforward — yields, ratios, datos de mercado — las resuelve bien. También funciona con comparativas, series temporales simples, y consultas de concepto. Si sabes lo que buscas pero no sabes cómo pedírselo al terminal, AskB te ahorra un tiempo considerable.

**Sin necesidad de saber fórmulas.** Para alguien que viene del mundo de la programación y los datos, pero no ha crecido con el terminal, esto reduce enormemente la fricción de entrada.

## Lo que no funciona tan bien

**Consultas ambiguas.** Si la pregunta no está bien definida, AskB te devuelve resultados que no son lo que pedías. No tiene buen mecanismo para pedir clarificación — asume que entendió y devuelve algo. A veces devuelve algo completamente distinto a lo que esperabas.

**Profundidad analítica limitada.** Para consultas superficiales — datos puntuales, comparativas rápidas, información de mercado general — funciona muy bien. Cuando necesitas análisis más elaborado, necesitas volver al terminal clásico y procesar tú.

**Dependencia de la calidad de la pregunta.** Es muy sensible a cómo formulas la pregunta. Una consulta mal planteada produce resultados inútiles, y no siempre es obvio cómo reformularla.

**Contexto limitado.** No mantiene memoria de la conversación. Cada pregunta es independiente, así que no puedes encadenar un análisis complejo en varios pasos sin repetir contexto.

## Mi opinión después de unos meses

AskB no es revolución. No está reemplazando cómo trabajo con el terminal — está reduciendo el coste de acceso a consultas simples y medias. Donde antes me tomaba 5 minutos buscar un dato y armarlo, ahora lo hago en 30 segundos.

Lo que más valoro es el acceso remoto. Terminal Anywhere + AskB significa que puedo consultar datos de mercado sin estar delante de mi máquina. Para un workflow que implica revisar posiciones, comparar métricas y hacer seguimiento de riesgos, esto importa.

Donde me pierdo es cuando el trabajo requiere análisis más complejo. Ahí vuelvo a Python, a mis propios scripts, a la potencia de procesamiento que necesito para modelos de riesgo o estudios cuantitativos. AskB es una herramienta de acceso y consulta, no de análisis.

## En resumen

Si trabajas con Bloomberg y no lo has probado: pruébalo. No te va a cambiar el workflow de forma dramática, pero sí te va a ahorrar tiempo en las consultas que haces constantemente.

Si trabajas en remoto y usas Terminal Anywhere: AskB es razón suficiente para usarlo más veces de las que usabas el terminal antes.

No es el futuro del análisis financiero. Es el presente del acceso a datos financieros — más rápido, más accesible, y con margen claro de mejora.

---

*¿Lo estás usando tú también? Cuéntame tu experiencia en los comentarios.*