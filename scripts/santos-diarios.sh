#!/bin/bash
# Script para obtener los santos del día y enviarlos por Telegram

# Obtener fecha actual
DIA=$(date +%-d)
MES=$(date +%-m)

# URL del santoral
URL="https://www.aciprensa.com/santos/mes/$MES"

# Obtener página web
CONTENT=$(curl -s "$URL" 2>/dev/null)

# Extraer los santos del día actual
# Buscar la sección del día actual
SAINTS=$(echo "$CONTENT" | grep -A 50 "$DIA $MES" | head -40 | sed -n '/<h3\|<h4\|<li/p' | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/&amp;/\&/g' | tr -s '\n' | head -20)

# Si no encontró saints hoy, usar el primer día del mes
if [ -z "$SAINTS" ]; then
    SAINTS="No se encontraron santos para hoy."
fi

# Enviar a Telegram (aquí iría el código del bot)
echo "$SAINTS" > /tmp/santos-hoy.txt
echo " Santos del $(date +%-d/%-m): $(cat /tmp/santos-hoy.txt)"
