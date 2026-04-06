# Informe: Mejoras y Skills para OpenClaw

**Fecha:** 2026-04-06  
**Contexto:** OpenClaw 2026.4.5, VPS Linux, Telegram como canal principal

---

## 1. Standing Orders (ya disponibles, sin usar)

**Descripción:** Autoridad operativa permanente para tareas recurrentes. Se define en AGENTS.md o un archivo dedicado y el agente ejecuta de forma autónoma dentro de esos límites, combinados con cron jobs.

**Qué resuelve:** Actualmente los crons disparan prompts que explican qué hacer cada vez. Con standing orders, defines "esto es tu responsabilidad permanente" y solo escalas cuando hay excepciones.

**Compatibilidad:** 100% — solo configuración y archivos de workspace.

**Riesgos:** Muy bajos. Es documentación interna que guía al agente.

**Recomendación: INSTALAR** — Mejora la autonomía y reduce la fricción de los crons actuales. Podríamos definir standing orders para:
- Gestión de inbox (qué hacer con emails nuevos)
- Seguimiento de proyectos activos
- Revisión periódica de memoria

---

## 2. Dreaming / Consolidación de memoria (experimental)

**Descripción:** Sistema de consolidación de memoria en background que promotiona automáticamente contenido de short-term a long-term (MEMORY.md) usando scoring con umbrales.

**Qué resuelve:** La memoria se llena de notas diarias que nunca se depuran. Dreaming hace el trabajo sucio de decidir qué merece quedarse en MEMORY.md.

**Compatibilidad:** Linux/VPS — requiere el plugin `memory-core` y un embedding provider (no configurado actualmente según MEMORY.md).

**Riesgos:** Experimental. Podría promover cosas que no deben ir a largo plazo.

**Recomendación: BAJO CONSIDERACIÓN** — Interesante para memoria automática, pero requiere embedding provider (OpenAI/Gemini/Mistral) que no tenemos configurado. Si Paduel quiere invertir en esto, hay que añadir una API key de embeddings. Si no, el mantenimiento manual de MEMORY.md funciona bien.

---

## 3. Memory Search con embeddings (habilitado)

**Descripción:** `memory_search` usa búsqueda híbrida (vector + keyword) cuando hay embedding provider. Actualmente **NO está activo** porque no hay API key de embeddings configurada.

**Compatibilidad:** Requiere API key de OpenAI/Gemini/Voyage/Mistral.

**Riesgos:** Ninguno — es un opt-in.

**Recomendación: BAJO CONSIDERACIÓN** — Si tenemos API key de algún embedding provider, merece la pena activarlo. Mejora mucho la calidad de `memory_search` (encuentra cosas aunque cambies la redacción).

---

## 4. Hooks para webhooks externos

**Descripción:** OpenClaw puede recibir webhooks externos y actuar sobre ellos. Ejemplo: cuando ocurre un evento en un servicio externo, envía un POST a `/hooks/wake` y el agente recibe un system event.

**Qué resuelve:** Integración con servicios que no tienen canal propio (Twitter, APIs personalizadas, sistemas de monitoring...).

**Compatibilidad:** Requiere endpoint público o acceso vía Tailscale. Este VPS tiene Tailscale configurado según MEMORY.md.

**Riesgos:** Seguridad si se expone mal — pero tiene auth token y reject de paths generales.

**Recomendación: BAJO CONSIDERACIÓN** — Potente para automatización avanzada. Si Paduel tiene servicios específicos que quiere integrar, vale la pena. Para uso general, es overkill.

---

## 5. Healthcheck Skill (ya disponible en el sistema)

**Descripción:** Skill de hardening de seguridad y configuración de salud del sistema para la máquina que corre OpenClaw.

**Qué resuelve:** Auditorías de seguridad, hardenizado SSH/firewall, revisión de exposición.

**Compatibilidad:** Linux/VPS — perfecto para este entorno.

**Riesgos:** Ninguno — es auditoría y consulta.

**Recomendación: INSTALAR** — Ya existe en el sistema, solo necesita ejecutarse. Muy útil para tener visibilidad del estado de seguridad del VPS. Podemos lanzarlo cuando queramos con `openclaw health`.

---

## 6. ComfyUI Plugin (nuevo en 2026.4.5)

**Descripción:** Workflow de imagen, vídeo y música local a través de ComfyUI o Comfy Cloud. Incluye `image_generate`, `video_generate`, y `music_generate`.

**Qué resuelve:** Generación multimedia sin depender de APIs externas (costosas).

**Compatibilidad:** Requiere ComfyUI local o cuenta de Comfy Cloud. En VPS sin GUI esto no es viable para generación local.

**Riesgos:** Instalación compleja si se quiere local.

**Recomendación: NO INSTALAR** — En VPS este feature no es usable. Si Paduel tiene ComfyUI en otra máquina, sería vía API endpoint, pero ya tenemos MiniMax para generación.

---

## 7. Video Generation vía MiniMax/xAI/Wan (ya disponible)

**Descripción:** Generación de vídeo nativa desde la 2026.4.5. Disponible a través de `video_generate`.

**Compatibilidad:** Requiere provider configurado (MiniMax, xAI Grok, o Alibaba Wan).

**Riesgo:** No tenemos API keys para estos providers.

**Recomendación: BAJO CONSIDERACIÓN** — Si MiniMax permite generación de vídeo, podría ser interesante. Requiere investigar si MiniMax tiene ese endpoint y si tenemos acceso.

---

## 8. Standing Orders: Inbox Triage (nuevo skill)

**Descripción:** Hay un skill `clawflow-inbox-triage` disponible en el sistema que demuestra cómo triar mensajes por intención, con diferentes rutas (notificar inmediatamente, esperar respuesta externa, resumir después).

**Qué resuelve:** Automatización inteligente de inbox. Muy útil para emails o mensajes que requieren diferentes tratamientos.

**Compatibilidad:** 100% compatible con el entorno.

**Riesgos:** Ninguno.

**Recomendación: INSTALAR** — Es un ejemplo de patrón muy útil. Podemos usarlo como base para un inbox triage real (email u otras fuentes).

---

## 9. Whisper STT (ya disponible)

**Descripción:** Transcripción local de audio con Whisper. Ya sabemos que existe pero no lo hemos usado nunca.

**Compatibilidad:** Ya instalado en el VPS.

**Riesgos:** Sin GPU, lento en audios largos (>5 min).

**Recomendación: INSTALAR** — Ya lo tenemos. Simplemente hay que usarlo cuando Paduel mande audios por Telegram.

---

## 10. Webhooks como delivery (ya disponible)

**Descripción:** Los cron jobs pueden entregar a un webhook en vez de a un canal. Esto permite integrar con sistemas externos (Zapier, Make, Discord webhooks, etc.).

**Compatibilidad:** 100%.

**Riesgos:** Muy bajos.

**Recomendación: BAJO CONSIDERACIÓN** — Depende de si hay servicios externos con los que integrar.

---

## 11. Ollama para modelos locales

**Descripción:** Provider para Ollama (modelos locales como Llama, Qwen, etc.).

**Qué resuelve:** Independencia de APIs externas para ciertos tareas. Menor coste.

**Compatibilidad:** Requiere Ollama instalado en algún sitio (VPS o máquina local con API accessible).

**Riesgos:** Calidad variable según modelo.

**Recomendación: NO INSTALAR** — Ya tenemos MiniMax con 1500 llamadas por ventana de 5h y semanal ilimitado. No hay presión de coste. Mantener para cuando MiniMax falle o se agote.

---

## Resumen de recomendaciones

| Mejora | Recomendación | Razón |
|---|---|---|
| Standing Orders | **INSTALAR** | Autonomía, ya disponible, sin riesgo |
| Healthcheck (skill) | **INSTALAR** | Ya existe, auditoría de seguridad del VPS |
| Whisper STT | **INSTALAR** | Ya disponible, usar cuando mande audios |
| Inbox Triage (clawflow) | **INSTALAR** | Patrón útil como referencia |
| Dreaming | **BAJO CONSIDERACIÓN** | Experimental, requiere embeddings |
| Memory Search con embeddings | **BAJO CONSIDERACIÓN** | Requiere API key de embeddings |
| Hooks/Webhooks | **BAJO CONSIDERACIÓN** | Automatización avanzada |
| ComfyUI | **NO INSTALAR** | No viable en VPS headless |
| Ollama | **NO INSTALAR** | MiniMax cubre bien las necesidades |
| Video Generation | **NO INSTALAR** | Sin provider disponible |

---

## Próximos pasos sugeridos

1. **Ahora:** Añadir Standing Orders al AGENTS.md para formalizar las responsabilidades autónomas
2. **Ahora:** Hacer un healthcheck del VPS con el skill existente
3. **Antes del próximo mes:** Activar dreaming si conseguimos API key de embeddings, o decidir que el mantenimiento manual de MEMORY.md es suficiente
