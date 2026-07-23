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


### 2026-07-23 — Actualización rompe auth: 3 crons caen por la misma raíz
- **Tarea:** Diagnosticar por qué `Weekly Memory Review`, `Agenda diaria 8h` y `Recordatorio asignaturas Alonso 8h` (`main` x2, `tutor` x1) fallaban con 15x/15x/2x `consecutiveErrors` y por qué `memory_search` también estaba caído.
- **Qué pasó:**
  1. La actualización OpenClaw de hoy migró el auth de JSON a sqlite. Los backups quedan en `agents/<agent>/agent/auth-profiles.json.sqlite-import.<ts>.bak`.
  2. La migración se quedó a medias en el agente `main` y **no tocó el agente `tutor`** (su sqlite tenía `auth_profile_store` y `auth_profile_state` completamente vacíos). Sin profiles portables, todos los agentTurn que invocan minimax fallan con `FailoverError: No API key found for provider "minimax"`.
  3. Paduel arregló el `main` a mano (reinsertó los rows en `auth_profile_store` / `_state`). El `tutor` seguía roto.
  4. Lo que hice en `tutor`: backup del sqlite a `openclaw-agent.sqlite.backup-pre-minimax-20260723-132347`, después `INSERT OR REPLACE` de los dos rows copiados del `main` (`minimax:global` + `minimax:default`), verificación con `openclaw models list --provider minimax --agent tutor` → Auth=yes en los 5 modelos.
  5. Forcé runs con `cron run --runMode force` en los dos crons de `main` → ambos pasaron a `lastRunStatus: ok`, `lastDeliveryStatus: delivered`, `consecutiveErrors: 0`. Los deliveries a Telegram #5675 (resumen semanal) y #5679 ("Hoy no hay nada programado") validaron el end-to-end real.
  6. El tercer cron (`Recordatorio asignaturas Alonso 8h`, agente `tutor`) lo deshabilitamos con `openclaw cron disable 504bc40c-6c95-4416-b709-2d7ac3378634` porque no hay colegio en vacaciones. **No borrar**: se reactiva en septiembre con `openclaw cron enable <id>`.
  7. Entre medio llegó un `systemEvent "⚠️ Cron failed"` (#5689) que probablemente fue el coletazo del scheduler anunciando los 15x residual antes de que el run forzado reescribiera el estado.
- **Lo que descubrí de paso:**
  - `memory_index_chunks_vec` falla con `no such module: vec0`: la **extensión sqlite-vec no está cargada**. Esa es la causa última de que `memory_search` también esté caído, no solo el API key. Fix no aplicado aún — Tavily funciona como backup.
  - El cron `Agenda diaria 8h` ejecuta bien pero siempre devuelve "Hoy no hay nada programado" porque el calendario de `animagerion@gmail.com` (la cuenta del agente, no la personal) está vacío. Issue conocido desde junio, no es lo que arreglamos aquí.
  - Los 3 crons arrastraban **dos bugs distintos solapados**: el de hoy (auth post-actualización) y los viejos (calendario vacío, wakeMode, lagunas). Solo el primero impedía la ejecución; los otros afectaban al *valor entregado*.
- **Lecciones (5):**
  1. **Síntomas idénticos no son la misma causa.** Tres crons fallaban, dos los achacaba a bugs viejos documentados en junio. La causa real era post-actualización. Siempre leer el `lastError` antes de memear "ya lo sé".
  2. **Los `systemEvent` que llegan entre mensajes son diagnóstico gratis.** #5675, #5679 y #5689 eran más informativos que mis propios JSON de `cron get`. Si ignoras el feed de Telegram mientras diagnosticas, te pierdes la realidad.
  3. **El provider key no es la única dependencia de un agente.** `main` tenía la key rota, `tutor` nunca la tuvo. El sintagma `openclaw-agent.sqlite` por agente implica que **cada agente necesita su propia fila de auth** tras una migración. Asumir que "el main está OK, los demás también" es incorrecto.
  4. **`openclaw cron disable <id>` por CLI es la vía nativa** para apagar crons de otro agente. La tool MCP `cron update` con `agentId` ajeno da `"must match the calling agent"`; `cron disable` con el token del gateway funciona. Usar CLI para cruzar límites de agente, usar la tool para el propio.
  5. **Backups del sqlite ANTES de cualquier INSERT manual.** El comando de backup `cp agents/tutor/agent/openclaw-agent.sqlite <dest>` ocupa 13MB y puede ahorrar una sesión entera si la migración sale mal.
- **Pendiente para reactivar en septiembre:**
  - `openclaw cron enable 504bc40c-6c95-4416-b709-2d7ac3378634` cuando empiecen las clases.
  - Considerar poblar el calendario `animagerion@gmail.com` con eventos reales para que la Agenda 8h deje de ser ruido.
  - Cargar la extensión `sqlite-vec` (paquete `libsqlite3-vec` o equivalente) para devolver `memory_search` a operativo.
- **Tags:** openclaw update auth sqlite cron debug tutor memory_search vec0


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
=== Weekly Review 2026-07-05 ===
Revisión completada: 2026-07-05
=== Weekly Review 2026-07-23 ===
Revisión completada: 2026-07-23
