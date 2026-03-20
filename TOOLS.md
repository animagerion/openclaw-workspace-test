# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

### TTS

- Preferred voice: "AlvaroNeutral" (Edge TTS, español)
- Channel: telegram (para formato correcto)

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## GitHub
- Credentials: /home/gerion/.openclaw/credentials/github.json

## MiniMax Token Usage
- Skill: `/home/gerion/.openclaw/workspace/skills/minimax-usage/`
- Script: `check_usage.sh` - Consulta uso de tokens del plan MiniMax
- Uso: `/home/gerion/.openclaw/workspace/skills/minimax-usage/check_usage.sh`
- API key: Obtenida automáticamente de `auth-profiles.json`
- Endpoint: `https://platform.minimax.io/v1/api/openplatform/coding_plan/remains`

