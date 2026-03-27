#!/bin/bash
# AI News Digest — Upload a Drive
# Sube el digest del día a la carpeta AI Weekly Digest y comparte enlace

GOG_KEYRING_PASSWORD="gerion-gog-2026"
SKILL_DIR="/home/gerion/.openclaw/workspace/skills/ai-news-digest"
DATE=$(date +%Y-%m-%d)
DIGEST_FILE="$SKILL_DIR/digest_$DATE.md"
DRIVE_FOLDER_ID="13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk"

if [ ! -f "$DIGEST_FILE" ]; then
    echo "❌ No existe $DIGEST_FILE"
    exit 1
fi

echo "📤 Subiendo digest a Drive (carpeta: AI Weekly Digest)..."
RESULT=$(GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" gog drive upload "$DIGEST_FILE" --parent "$DRIVE_FOLDER_ID" --account animagerion@gmail.com --no-input 2>&1)
echo "$RESULT"

FILE_ID=$(echo "$RESULT" | grep -oP 'id\s+\K\S+' | head -1)
echo "📁 File ID: $FILE_ID"

if [ -n "$FILE_ID" ]; then
    echo "🔗 Generando enlace compartible..."
    GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" gog drive share "$FILE_ID" --type anyone --role reader --account animagerion@gmail.com --no-input 2>&1
    LINK=$(GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" gog drive url "$FILE_ID" --account animagerion@gmail.com --no-input 2>&1 | grep -oP 'https://[^\s]+' | head -1)
    echo "✅ Enlace: $LINK"
else
    echo "⚠️ No se pudo obtener el file ID"
fi
