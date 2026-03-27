#!/bin/bash
# AI News Digest — Cron wrapper
# Se ejecuta cada noche. Recopila artículos y lanza subagente para redactar + editar + subir.
set -e

SKILL_DIR="/home/gerion/.openclaw/workspace/skills/ai-news-digest"
DATE=$(date +%Y-%m-%d)

# 1. Recopilar
python3 "$SKILL_DIR/collect.py"

# 2. Lanzar subagente con los artículos para que redacte, edite y suba
openclaw session spawn \
  --label "ai-digest-$DATE" \
  --runtime subagent \
  --mode run \
  --timeout 600 \
  --task "
  Eres el editor del AI Weekly Digest.

  1. Lee los artículos recopilados en: /home/gerion/.openclaw/workspace/skills/ai-news-digest/articles.md
  2. REDACTA un digest en español de ~1000 palabras siguiendo esta estructura:
     - **Ecosistema AI**: movimientos, announcements, modelos nuevos
     - **Empresas y Valoraciones**: financiación, M&A, resultados
     - **Aplicaciones Empresariales**: casos de uso reales
     - **Maker / Open Source**: proyectos, herramientas
     - **Finanzas**: stocks AI, VC funding, mercado
  3. Guarda el digest en: /home/gerion/.openclaw/workspace/skills/ai-news-digest/digest_$(date +%Y-%m-%d).md
  4. EJECUTA /home/gerion/.openclaw/workspace/skills/ai-news-digest/upload.sh para subirlo a Drive
  5. Envía a Paduel por Telegram el enlace de Drive: https://drive.google.com/drive/folders/13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk
     Usa el message tool con action=send, channel=telegram
  6. Confirma cuando esté hecho.
  " 2>&1

echo "✅ Subagente lanzado. Te notificará cuando termine."
