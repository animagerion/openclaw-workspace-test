# Learnings.md - Aprendiendo de la experiencia

## ¿Cómo usarlo?
- Después de tareas complejas o errores, anota aquí qué salió bien y qué no
- Cada entrada lleva fecha y contexto
- Las entradas importantes se incorporan a MEMORY.md en la revisión semanal

---

## Entradas

### 2026-06-08 — Hipoclorito piscina: precio local ya es competitivo
- **Tarea:** Investigar alternativas online más baratas para hipoclorito sódico 25kg
- **Qué pasó:** Investigación online: el más barato en península sale ~32-35€ con envío vs 18€ en tienda local del usuario. Seven Pools Canarias (17,50€) no compensa por portes. Bunzl/Jofisa B2B podrían dar 12-15€/ud en palé de 4-6.
- **Lección:** Para productos químicos pesados/regulados, el 'más barato online' rara vez compite con tienda local por portes+restricciones. La economía solo aparece a partir de 4-6 unidades (descuento B2B por palé).
- **Tags:** compra investigacion piscina


### 2026-06-08 — Cron agenda diaria funciona pero calendario vacío
- **Tarea:** Diagnosticar por qué la agenda diaria siempre dice 'no hay nada'
- **Qué pasó:** El cron de las 8h ejecuta bien y entrega, pero el calendario de animagerion@gmail.com (cuenta del agente) está prácticamente vacío. Por eso siempre devuelve 'Hoy no hay nada programado' y el usuario percibe que no recibe nada.
- **Lección:** Un cron que se ejecuta correctamente puede parecer roto al usuario si la fuente de datos está vacía. Antes de optimizar el delivery, validar que el contenido existe. La cuenta 'animagerion@gmail.com' no es la personal del usuario.
- **Tags:** gog calendario cron debug


### 2026-06-08 — Santos diarios: cron se ejecuta pero trigger no llega a Telegram
- **Tarea:** Diagnosticar por qué no se reciben los santos diarios en Telegram
- **Qué pasó:** El cron Santos Diarios se ejecuta ok (lastRunStatus=ok) y el script devuelve contenido válido. Pero el systemEvent SANTOS_TRIGGER con wakeMode 'next-heartbeat' no se procesa en la sesión principal si la sesión está dormida.
- **Lección:** Para systemEvents críticos (no opcionales), usar wakeMode='now' en vez de 'next-heartbeat'. Next-heartbeat depende de que la sesión esté activa cuando llegue el trigger, lo cual no es fiable a las 7:00 UTC.
- **Tags:** cron telegram openclaw debug


### 2026-06-08 — Sistema de captura de aprendizajes creado
- **Tarea:** Implementar sistema de auto-captura de learnings + weekly review con detección de lagunas
- **Qué pasó:** Creado scripts/log_learning.sh para entradas consistentes con formato título/tarea/qué-pasó/lección/tags. Mejorado scripts/weekly-memory-review.sh para comparar git log vs learnings y avisar de lagunas.
- **Lección:** El problema 'no se documentan aprendizajes' se resuelve con (1) herramienta de bajo overhead para capturar y (2) detección automática de lagunas en el review semanal. Sin la segunda, la primera no se usa por olvido.
- **Tags:** meta memoria workflow openclaw


### 2026-06-08 — Actualización OpenClaw fallida por disco
- **Tarea:** Actualizar OpenClaw 2026.4.15 a 2026.6.1 vía openclaw update
- **Qué pasó:** El comando openclaw update imprime solo 'Updating OpenClaw...' y sale con 0 sin aplicar la nueva versión. Disco al 83% (6.2 GB libres). El gateway se auto-restartó tras el intento.
- **Lección:** Cuando openclaw update se queda colgado en silencio, comprobar espacio en disco ANTES de reintentar. Una salida vacía con exit 0 es peor que un error visible.
- **Tags:** openclaw update disco debug


<!-- Las lecciones significativas se mueven a MEMORY.md tras la revisión semanal -->=== Weekly Review 2026-04-19 ===
Revisión completada: 2026-04-19
=== Weekly Review 2026-04-26 ===
Revisión completada: 2026-04-26
=== Weekly Review 2026-05-03 ===
Revisión completada: 2026-05-03
=== Weekly Review 2026-05-10 ===
Revisión completada: 2026-05-10
=== Weekly Review 2026-05-17 ===
Revisión completada: 2026-05-17
=== Weekly Review 2026-05-24 ===
Revisión completada: 2026-05-24
=== Weekly Review 2026-05-31 ===
Revisión completada: 2026-05-31
=== Weekly Review 2026-06-07 ===
Revisión completada: 2026-06-07
=== Weekly Review 2026-06-08 ===
Revisión completada: 2026-06-08
=== Weekly Review 2026-06-14 ===
Revisión completada: 2026-06-14
=== Weekly Review 2026-06-21 ===
Revisión completada: 2026-06-21
=== Weekly Review 2026-06-28 ===
Revisión completada: 2026-06-28
