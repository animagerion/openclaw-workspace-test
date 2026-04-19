# Guía Avanzada de OpenClaw — Potenciando tu Agent

*Generado: 2026-04-19 | Basado en docs oficiales y casos reales*

---

## Por Qué Esta Guía

El artículo anterior era genérico y سطححي. Esto va de lo que realmente podemos implementar en nuestro setup actual. Cada sección incluye: qué es, por qué importa, cómo lo instalamos, y enlaces a la documentación oficial.

---

## 1. Sistema de Memoria — Profundidad

### 1.1 Memoria Activa (Active Memory)

**Qué es:** Un sub-agente de memoria que busca contexto relevante *antes* de cada respuesta, en lugar de esperar a que le pidamos "recuerda esto".

**Por qué importa:** El agente no necesita que le digas "según lo que hablamos ayer..." — busca en memoria automáticamente.

**Cómo funciona:**
- Plugin `active-memory` inyecta un resumen de memoria en el prompt antes de cada respuesta
- Modelo dedicado (opcional): usa Cerebras GPT OSS 120B para baja latencia
- Solo corre en DMs, configurable por tipo de chat

**Instalación:**
```json
{
  "plugins": {
    "entries": {
      "active-memory": {
        "enabled": true,
        "config": {
          "enabled": true,
          "agents": ["main"],
          "allowedChatTypes": ["direct"],
          "modelFallback": "minimax/MiniMax-M2.1",
          "queryMode": "recent",
          "promptStyle": "balanced",
          "timeoutMs": 15000,
          "maxSummaryChars": 220
        }
      }
    }
  }
}
```

**Comandos útiles:**
```
/active-memory status   # Ver estado
/active-memory off     # Pausar en sesión actual
/active-memory on      # Reanudar
/verbose on            # Ver info de Active Memory en replies
/trace on              # Debug detallado
```

**Alternativa rápida (latencia mínima):** Dejar `config.model` sin fijar — hereda el modelo de la sesión actual (MiniMax M2.7).

📖 [Active Memory Docs](https://docs.openclaw.ai/concepts/active-memory.md)

---

### 1.2 Dreaming — Consolidación Automática de Memoria

**Qué es:** Un proceso en segundo plano que revisa las notas diarias y promocióna solo lo relevante a MEMORY.md.

**Por qué importa:** No tenemos que editar MEMORY.md manualmente — el sistema aprende qué merece persistir.

**Cómo funciona:**
- Recoge señales de corto plazo (frecuencia, diversidad, relevancia)
- Solo promocióna si pasa umbrales de calidad
- Escribe un diary en `DREAMS.md` para revisión humana
- Opt-in: desactivado por defecto

**Para activar:**
```bash
openclaw memory dreaming --enable
openclaw memory dreaming --schedule "0 2 * * *"  # nightly a las 2am
```

**Backfill histórico:**
```bash
# Revisar notas antiguas y promover candidatos
openclaw memory rem-backfill --path ./memory --stage-short-term

# Rollback si no fue útil
openclaw memory rem-backfill --rollback
```

📖 [Dreaming Docs](https://docs.openclaw.ai/concepts/dreaming.md)

---

### 1.3 Memory Wiki — Base de Conocimiento Compilada

**Qué es:** Compila MEMORY.md en una wiki estructurada con claims, evidencia, y tracking de contradicciones.

**Por qué importa:** Pasamos de notas informales a conocimiento versionado, auditable, y queryable.

**Características:**
- Estructura determinista de páginas
- Dashboard de freshness y contradicciones
- Compatible con Obsidian
- Genera digests para el agente

📖 [Memory Wiki Docs](https://docs.openclaw.ai/plugins/memory-wiki)

---

### 1.4 QMD Memory Engine — Búsqueda Híbrida Local

**Qué es:** Motor de búsqueda vectorial local + keyword matching + reranking.

**Por qué importa:** Búsqueda semántica real en nuestra propia base de conocimiento. No dépende de API externa.

**Setup (para búsqueda local activa):**
```bash
openclaw memory status  # Ver estado del índice
openclaw memory index --force  # Rebuild index
```

📖 [QMD Docs](https://docs.openclaw.ai/concepts/memory-qmd)

---

### 1.5 Honcho Memory — Memoria Cross-Session IA-Nativa

**Qué es:** Sistema de memoria con user modeling, búsqueda semántica, y consciencia multi-agente.

**Por qué importa:** Modela patrones del usuario automáticamente — aprende preferencias, estilo, contexto.

📖 [Honcho Docs](https://docs.openclaw.ai/concepts/memory-honcho)

---

## 2. Búsqueda Web —垂涎三尺 now (Lo Que Realmente Necesitamos)

### 2.1 Tavily Search Skill

**Qué es:** Skill oficial para búsqueda web con Tavily API.

**Por qué importa:** Resuelve el problema de que Brave Search no funciona sin API key configurada.

**API Key:** https://tavily.com — 1000 búsquedas/mes gratis

**Instalación:**
```bash
openclaw skills install tavily-search
```

**Config:**
```json
{
  "models": {
    "providers": {
      "tavily": {
        "apiKey": "${TAVILY_API_KEY}"
      }
    }
  }
}
```

📖 [Tavily](https://tavily.com)

---

### 2.2 Multi-Search Engine Skill

**Qué es:** Busca en múltiples motores simultáneamente sin API key.

**Por qué importa:** Sin límite de uso, sin coste.

**Instalación:**
```bash
openclaw skills install multi-search-engine
```

📖 [ClawHub — Multi-Search](https://clawhub.ai/skills)

---

## 3. Skills — Ecosistema

### 3.1 Skills Recomendados para Nuestro Setup

| Skill | Qué hace | Prioridad |
|---|---|---|
| **tavily-search** | Búsqueda web estructurada | ALTA |
| **multi-search-engine** | Búsqueda multi-motor sin API key | ALTA |
| **summarize** | Resume PDFs, webs, imágenes | MEDIA |
| **weather** |already installed | — |
| **gog** |already installed | — |

### 3.2 Buscar Skills

```bash
openclaw skills search "web search"
openclaw skills search "pdf"
openclaw skills search "research"
openclaw skills search --limit 20 --json
```

### 3.3 Instalar / Actualizar

```bash
openclaw skills install <slug>
openclaw skills update <slug>
openclaw skills update --all  # Actualizar todos
openclaw skills list --eligible  # Ver instalados
```

📖 [Skills CLI Docs](https://docs.openclaw.ai/cli/skills)
📖 [Skills System](https://docs.openclaw.ai/tools/skills)

---

## 4. Standing Orders — Lo Que Ya Hacemos (Pero Mejor)

### 4.1 Programa: Inbox Triage

Ya tenemos esto implementado (Gmail cada 30 min). Podemos mejorarlo:

**Mejoras posibles:**
- Añadir categorización automática (urgente/no urgente/marketing)
- Detectar threads que necesitan respuesta
- Resumen ejecutivo en vez de lista

### 4.2 Programa: Memoria Activa

Integrar Active Memory en nuestros standing orders:
- Antes de cada respuesta: buscar contexto relevante
- Después de decisiones importantes: escribir a MEMORY.md
- Revisión semanal de daily notes → promoción a long-term

### 4.3 Programa: Wellness Check

**Añadir:**
- Revisión de salud del sistema (openclaw health)
- Check de créditos MiniMax
- Verificación de auto-commit status

📖 [Standing Orders Docs](https://docs.openclaw.ai/automation/standing-orders.md)

---

## 5. Multi-Agente — Escalabilidad

### 5.1 Cuándo Merece la Pena

- **Varios usuarios** comparten gateway (familia, equipo)
- **Aislamiento de contexto** entre proyectos
- **Personalidades distintas** por canal o persona

### 5.2 Nuestro Caso: Alonso

Podríamos crear un agente dedicado para Alonso con:
- SOUL.md adaptado (más paciente, educativo)
- Memoria separada (progreso escolar, áreas de mejora)
- Skills específicos (generación de quizzes, ayuda con deberes)

**Setup básico:**
```bash
openclaw agents add alonso
```

**Binding para Telegram:**
```json
{
  "agents": {
    "list": [
      { "id": "main", "workspace": "~/.openclaw/workspace" },
      { "id": "alonso", "workspace": "~/.openclaw/workspace-alonso" }
    ]
  },
  "bindings": [
    {
      "agentId": "alonso",
      "match": {
        "channel": "telegram",
        "peer": { "kind": "direct", "id": "8689968236" }
      }
    }
  ]
}
```

📖 [Multi-Agent Docs](https://docs.openclaw.ai/concepts/multi-agent.md)

---

## 6. Casos de Uso Avanzados

### 6.1 Research Agent

```
Usuario → "Investiga sobre X" 
  → Sub-agent isolated (web fetch + synthesize)
  → Reporte estructurado en memoria
  → Usuario recibe resumen + enlaces
```

**Implementación:** Cron agentTurn con prompt de investigación, modelo MiniMax.

### 6.2 Weekly Digest

```
Cada domingo → Cron job
  → Resume week's conversations
  → Compila tasks pendientes
  → Genera digest
  → Envía por Telegram
```

**Ya lo hacemos parcialmente con los heartbeats. Podemos formalizarlo.**

### 6.3 Tutor Personal (para Alonso)

```
DeepTutor en portátil Windows:
  → WSL2 + Python
  → Conexión a MiniMax API
  → Interfaz web local

OpenClaw como backend:
  →记忆 del estudiante (nivel, temas, progreso)
  → Generación de quizzes
  → Recomendación de temas
  → Dashboard en móvil (Telegram)
```

📖 [DeepTutor Repo](https://github.com/HKUDS/DeepTutor)

---

## 7. Cosas Que Podemos Implementar Ya

### Inmediato (esta semana)

- [ ] **Active Memory plugin** — Configurar y activar
- [ ] **Dreaming** — Habilitar consolidación automática
- [ ] **Tavily API key** — Obtener e instalar skill de búsqueda
- [ ] **Multi-Search Engine** — Sin API key, instalar ahora

### Corto Plazo (próximo mes)

- [ ] **Memory Wiki** — Compilar nuestra base de conocimiento
- [ ] **QMD index** — Habilitar búsqueda vectorial local
- [ ] **Agente Alonso** — Setup básico multi-agente
- [ ] **Research cron** — Sub-agent para deep research

### Medio Plazo

- [ ] **DeepTutor + OpenClaw** — Integración para Alonso
- [ ] **Weekly digest** — Automatizar resumen semanal
- [ ] **Dashboard** — Control UI como panel de control

---

## 8. Enlaces Rápidos

### Documentación
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Full Index (LLMs.txt)](https://docs.openclaw.ai/llms.txt)
- [Features](https://docs.openclaw.ai/concepts/features)
- [Memory Overview](https://docs.openclaw.ai/concepts/memory.md)
- [Active Memory](https://docs.openclaw.ai/concepts/active-memory.md)
- [Dreaming](https://docs.openclaw.ai/concepts/dreaming.md)
- [Multi-Agent](https://docs.openclaw.ai/concepts/multi-agent.md)
- [Standing Orders](https://docs.openclaw.ai/automation/standing-orders.md)
- [Skills CLI](https://docs.openclaw.ai/cli/skills)

### ClawHub
- [Skills Marketplace](https://clawhub.ai/skills)
- [Search Tavily](https://clawhub.ai/skills/tavily-search)
- [Search Multi-Engine](https://clawhub.ai/skills/multi-search-engine)

### Repos
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [DeepTutor (HKUDS)](https://github.com/HKUDS/DeepTutor)
- [DeerFlow](https://github.com/bytedance/deer-flow)

### Providers
- [Tavily API](https://tavily.com) — 1000 searches/month gratis
- [Cerebras](https://cerebras.ai) — Modelos ultra-rápidos
- [MiniMax](https://platform.minimax.io) — Nuestro proveedor actual

---

## 9. Valoración Honest

| Funcionalidad | Estado Actual | Potencial |
|---|---|---|
| Memoria básica | ✅ MEMORY.md + daily | ✅++ Active Memory + Dreaming |
| Búsqueda web | ❌ Rota (sin Brave key) | ✅+ Tavily + Multi-Search |
| Skills | ✅ 6 instalados | ✅++ 52k+ disponibles |
| Multi-agente | ❌ No usado | ✅+ Agente Alonso |
| Standing Orders | ✅ 4 programas | ✅++ Formalizar +扩展 |
| Cron jobs | ✅ 4 activos | ✅++ Más research/tutor |
| Health monitoring | ⚠️ Manual | ✅++ Automatizado |

**El artículo genérico nos daba contexto. Esta guía nos da un roadmap.**

---

*¿Por dónde quieres empezar? Las opciones más rápidas de ganar son: (1) Instalar Tavily + Multi-Search, (2) Activar Active Memory, (3) Ambos.*
