# Browser Use — Skill para OpenClaw

## Skill oficial
- **ClawHub:** https://clawhub.ai/shawnpana/browser-use
- **GitHub:** https://github.com/browser-use/browser-use

## Qué es
CLI de automatización de navegador con más de 50ms de latencia por llamada. Permite:
- Abrir páginas, hacer click, escribir, scroll
- Extraer datos (html, text, title)
- Screenshots
- Gestionar cookies, tabs, sesiones
- Conectar a Chrome real del usuario (preserva logins)
- Navegador cloud (de pago)

## Instalación

### Opción 1: CLI como skill (local, gratuito)
1. `uvx browser-use install` → instala CLI
2. `browser-use doctor` → verificar
3. Instalar chromium headless (ver abajo)
4. SKILL.md ya incluye todos los comandos

### Opción 2: Cloud browser (de pago)
1. `browser-use cloud login <api-key>`
2. `browser-use cloud connect`
3. No necesita chromium local

## Chromium en VPS (headless)

###Instalar chromium:
```bash
# Ubuntu/Debian
apt install chromium-browser
# o
apt install chromium
```

Si no hay display, forzar modo headless:
```bash
export BROWSER_HEADLESS=true
# o al llamar
browser-use --headed open <url>  # NO para VPS sin display
```

Alternativa: browser-use cloud connect no necesita chromium local.

## Comandos útiles
```bash
browser-use open <url>           # Abrir página
browser-use state                 # Ver elementos clickables
browser-use click <index>        # Click por índice
browser-use input <index> "txt"  # Escribir en campo
browser-use screenshot [path]    # Captura
browser-use get title            # Título página
browser-use get html             # HTML completo
```

## Casos de uso
- Automatizar tareas web complejas (formularios multi-paso)
- Scraping de SPAs (JavaScript dinámico)
- Flujos que requieren login real (preservar cookies)
- Testing de webs
- Rellenar portales internos sin API

## Alternativas en ClawHub (gratis, local)
- `agent-browser-clawdbot`
- `browser-automation`
- `browser-automation-v2`

## Seguridad (según Tavily)
La skill da acceso amplio al navegador: cookies, sesión, JS execution, archivos locales. Usar perfil ephemeral o separado si se conectan cuentas sensibles. No conectar el perfil principal.

## Estado
- Fecha investigación: 2026-04-19
- chromium: NO instalado
- skill: NO instalada
- Decisión: posponer, revisar si surge necesidad concreta