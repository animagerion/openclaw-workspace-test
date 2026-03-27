#!/bin/bash
# AI News Digest — Orquestador
# 1. Recopila noticias
# 2. Gerion redacta
# 3. Subagente editor revisa
# 4. Sube a Drive
# 5. Envía enlace por Telegram

set -e
SKILL_DIR="/home/gerion/.openclaw/workspace/skills/ai-news-digest"
WORKSPACE="/home/gerion/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
DIGEST_FILE="$SKILL_DIR/digest_$DATE.md"
DRIVE_FOLDER_ID="13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk"

echo "🤖 AI News Digest — $(date)"
echo "================================"

# 1. Recopilar
echo "📡 Fase 1: Recopilando artículos..."
python3 "$SKILL_DIR/collect.py"

# 2. Check que hay artículos
ARTICLE_COUNT=$(grep -c "^###" "$SKILL_DIR/articles.md" 2>/dev/null || echo 0)
echo "📰 Artículos recopilados: $ARTICLE_COUNT"

if [ "$ARTICLE_COUNT" -lt 3 ]; then
    echo "⚠️ Muy pocos artículos, continuando de todas formas..."
fi

# 3. El digest ya está generado en articles.md — lo mostrarmos para context
echo ""
echo "📝 Fase 2: Generando digest..."
echo "   (Los artículos están en $SKILL_DIR/articles.md)"
echo ""
echo "   El digest se redacta en la sesión principal de Gerion."
echo "   Después se pasa al editor subagente."

# Mostrar los artículos para contexto
echo ""
echo "--- ARTÍCULOS RECOPILADOS ---"
cat "$SKILL_DIR/articles.md"
echo "--- FIN ARTÍCULOS ---"
