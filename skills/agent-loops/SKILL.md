---
name: agent-loops
description: "Diseña y monta loops agentic con verificación y stop conditions claras. Úsalo cuando Paduel pida automatizar algo recurrente, montar un cron con lógica, o convertir un flujo manual en uno auto-ejecutable. Inspirado en la guía oficial 'Getting started with loops' de @ClaudeDevs (7 julio 2026)."
---

# Agent Loops — Diseñar bucles que funcionan

## Filosofía base

> **No prompt-and-pray. Diseña un loop.**

Un loop agentic no es "ejecuta esto cada X minutos y reza". Es un bucle donde el agente tiene claras tres cosas:

1. **Qué hacer ahora** — siguiente paso atómico
2. **Cómo verificar su trabajo** — gate automático, no fe ciega
3. **Cuándo parar** — stop condition explícita

Si no puedes definir las tres, no es un loop: es wishful thinking. Sigue en modo prompt manual.

---

## Las 3 preguntas obligatorias antes de crear un loop

Responde ANTES de escribir nada:

| Pregunta | Si no puedes responderla... |
|---|---|
| ¿Qué trigger lo arranca? (evento, hora, cambio en un dato) | No hay loop. Solo hay un cron tonto. |
| ¿Cómo verifica que el trabajo quedó bien? | Vas a necesitar un humano revisando. Eso no es un loop. |
| ¿Cuál es la stop condition? | El agente va a iterar hasta gastarse el budget o degradarse. |

---

## Los 6 building blocks (de Eric Tech, alineados con Anthropic)

1. **Trigger** — qué dispara el loop (cron, webhook, cambio en archivo/API, evento de calendario, email recibido)
2. **Worktree / scope** — entorno donde trabaja (directorio aislado, sesión específica, contexto acotado)
3. **Skills** — capacidades que puede invocar (verificación incluida, no opcional)
4. **Connectors** — APIs externas que necesita (Gmail, Drive, calendario, etc.)
5. **Memory** — estado entre iteraciones (puede ser un archivo, un issue de GitHub, una tabla en Drive)
6. **Sub-agents** — paralelismo y delegación cuando la tarea lo pide

> **Regla de oro:** tu primer loop debe ser pequeño, de un solo propósito, y muy supervisado. Tu segundo loop se conecta al primero.

---

## Cuándo SÍ usar un loop

- Tarea repetitiva con verificación automática clara
- Datos de entrada estables y formato conocido
- Stop condition objetiva (tests pasan, X == Y, archivo existe, API devuelve 200)
- Falla silenciosa es peor que no hacerlo (monitorización, saneado)

## Cuándo NO usar un loop

- Decisiones creativas donde el humano debe juzgar dirección
- Output que va directamente al usuario sin filtro (newsletter personal, mensaje a un cliente)
- No puedes definir el stop condition → **no lo automatices**
- Es la primera vez que haces la tarea → primero hazla 2-3 veces manual

---

## Anatomía de un loop bien montado

```text
TRIGGER (cron / event)
  ↓
AGENT (contexto cargado, skill definida)
  ↓
ACCIÓN (1 paso atómico)
  ↓
VERIFICACIÓN (gate automático: test, check, diff, API call)
  ↓
¿Cumple stop condition?
  ├── Sí → FIN (commit, notifica, log)
  └── No → itera (con budget/iteraciones max)

Si supera N iteraciones → ESCALAR al humano (no fallar en silencio)
```

---

## Primitivas disponibles en OpenClaw

- **Cron con `wakeMode=now`** — dispara el loop
- **`sessionTarget=isolated` con `agentTurn`** — sesión fresca cada iteración (evita degradación de contexto)
- **`HEARTBEAT.md`** — para checks periódicos que viven en sesión main
- **Skills específicas del workspace** — como herramientas del loop
- **MEMORY.md** — memoria persistente entre iteraciones (estado, decisiones)
- **`subagents`** — paralelismo cuando una iteración tiene subtareas independientes
- **`failureAlert`** — escalación automática cuando el loop falla N veces seguidas

---

## Workflow para crear un loop nuevo

### 1. Especificación (responder antes de codear)

```markdown
## Loop: [nombre]
**Trigger:** [cron / webhook / file change / event]
**Acción:** [1 frase]
**Stop condition:** [cómo sabe que ha terminado]
**Verificación:** [cómo comprueba que el resultado es correcto]
**Output:** [a dónde va: telegram, commit, file, API]
**Escalación:** [qué hace si falla N veces]
**Budget:** [max iteraciones / max tokens / max tiempo]
```

### 2. Implementación
- Si es cron → `cron action=add` con `sessionTarget=isolated`
- Si es trigger reactivo → script con hook + `cron` de vigilancia
- Aislar contexto: pasar solo lo necesario al agente, no MEMORY.md entero
- Skill de verificación SIEMPRE (si no la hay, escríbela)

### 3. Supervisión humana
- Primera semana: revisar logs cada día
- Notificación por Telegram si supera N iteraciones o si el output es raro
- Kill switch: cómo pararlo (`cron action=remove` o flag en archivo)

### 4. Iteración
- Si falla mucho → ¿la verificación es demasiado estricta o demasiado laxa?
- Si itera sin parar → ¿la stop condition está mal definida?
- Si gasta mucho token → ¿estás pasando contexto de más?

---

## Anti-patrones (lo que NO debes hacer)

❌ **Cron sin verificación** — "ejecuta esto cada hora". Si falla, nadie se entera.
❌ **Loop sin stop condition** — el agente iterará hasta gastarse el budget o producir basura.
❌ **Loop sin budget** — sin max iteraciones o max tiempo, puede irse horas.
❌ **Pasar MEMORY.md entero al subagente** — contexto irrelevante = gasto + ruido.
❌ **Loop creativo** — escribir copy, tomar decisiones de diseño, hablar con clientes. Eso requiere humano.
❌ **Loops conectados sin supervision** — dos loops hablando entre sí sin gate humano = debugging nightmare.

---

## Ejemplos buenos en este workspace

- **Santos diarios** (cron 09:00) — trigger fijo, output validado, falla silenciosa tolerable
- **Agenda diaria** (cron 08:00) — trigger fijo, lee calendario (estado), output a Telegram
- **Auto-commit workspace** (cron cada 6h) — verifica si hay cambios antes de actuar, falla segura

## Ejemplos a MEJORAR (loops tontos actuales)

- **Check Gmail cada 30 min** — detecta nuevos pero no verifica, puede duplicar notificaciones si el contador falla
- Cualquier cron sin test automático → añadir skill de verificación

---

## Cuando Paduel pide "automatiza X"

1. Pregunta: ¿es repetitivo y verificable? → loop candidato
2. Si sí: rellena la especificación del punto 1 antes de codear
3. Si no: propon alternativa (script one-shot, skill puntual, prompt manual recurrente)

## Cuando Paduel dice "esto falla mucho" en un loop existente

1. Lee los runs del cron → `cron action=runs jobId=...`
2. ¿Falla en verificación o en stop condition?
3. ¿El agente itera sin converger? → stop condition mal definida
4. ¿Falla de entrada? → el trigger está mal (datos vacíos, race condition)
5. Documenta el fix en `memory/YYYY-MM-DD.md`

---

**Referencias:**
- @ClaudeDevs, "Getting started with loops" (7 julio 2026) — guía oficial Anthropic
- Eric Tech, "Claude Code Works Better With Loops, Not Prompts" (YouTube, jun 2026)
- Lenny's Newsletter, "How to design AI agent loops" (jun 2026)