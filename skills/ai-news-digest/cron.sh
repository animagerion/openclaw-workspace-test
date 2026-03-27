#!/bin/bash
# AI News Digest — Cron (noche)
# 1. Recopila artículos
# 2. Me avisa a Telegram para que yo redacte, edite y suba
set -e

SKILL_DIR="/home/gerion/.openclaw/workspace/skills/ai-news-digest"
DATE=$(date +%Y-%m-%d)

echo "📡 AI News Digest cron — $(date)"

/home/gerion/.openclaw/workspace/skills/ai-news-digest/collect.py

ARTICLE_COUNT=$(grep -c "^###" "$SKILL_DIR/articles.md" 2>/dev/null || echo 0)

echo "✅ Artículos recopilados: $ARTICLE_COUNT"
echo "📝 Fichero: $SKILL_DIR/articles.md"

# Enviar notificación a Paduel (a través del gateway local via curl)
# El message tool funciona desde dentro de OpenClaw, no desde cron externo
# Así que simplemente dejamos los artículos listos y lo annonciamos via Telegram bot API

CHAT_ID="257331761"
TELEGRAM_TOKEN=$(cat /home/gerion/.openclaw/config.yml 2>/dev/null | grep -oP 'telegram.*token:\s*\K\S+' | head -1 || echo "")

if [ -n "$TELEGRAM_TOKEN" ]; then
    curl -s "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=🤖 AI News Digest listo ($DATE). $ARTICLE_COUNT artículos en $SKILL_DIR/articles.md. Redacta el digest y súbelo a Drive cuando puedas." \
        -d "parse_mode=Markdown" 2>/dev/null
    echo "✅ Notificación enviada a Telegram"
else
    echo "⚠️ No se encontró token de Telegram en config.yml"
fi
