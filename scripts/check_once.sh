#!/bin/bash
# Comprueba resultado Cuponazo ONCE 27/03/2026
# Boleto: 70183, Serie: 025

GOG_KEYRING_PASSWORD="gerion-gog-2026"
TOKEN_PATH="/tmp/once_result.txt"
URL="https://www.elperiodicodeceuta.es/resultado-del-cuponazo-de-la-once-super-once-y-triplex-hoy-viernes-27-de-marzo-de-2026/"

echo "=== COMPROBANDO CUPONAZO ONCE 27/03/2026 ==="
echo "Boleto: 70183 | Serie: 025"
echo "URL: $URL"
echo ""

# Fetch result page
CONTENT=$(curl -s "$URL")

# Try to extract number and serie from the page
# The page has "Número premiada: XXXXX" and "Serie: XXX" placeholders
# Try a more specific search in case results are now published
NUM=$(echo "$CONTENT" | grep -oP '(?i)número.premiado[:\s]+([0-9]{5})' | head -1 | grep -oP '[0-9]{5}')
SER=$(echo "$CONTENT" | grep -oP '(?i)serie[:\s]+([0-9]{3})' | head -1 | grep -oP '[0-9]{3}')

echo "Número publicado: ${NUM:-no disponible}"
echo "Serie publicada: ${SER:-no disponible}"

if [[ "$NUM" == "70183" ]]; then
  if [[ "$SER" == "025" ]] || [[ "$SER" == "" ]]; then
    RESULTADO="🎉 ¡MEGA PREMIOS! ¡CUPONAZO CAÍDO! ¡NÚMERO 70183!"
  else
    RESULTADO="✅ ¡Premio! El número 70183 coincide pero serie diferente"
  fi
else
  RESULTADO="❌ No ha habido premio esta vez. ¡Mejor suerte mañana!"
fi

echo ""
echo "$RESULTADO"
echo "Verifica en: $URL"

# Guardar resultado
echo "$RESULTADO" > "$TOKEN_PATH"
echo "URL: $URL" >> "$TOKEN_PATH"
echo "Número publicado: ${NUM:-N/A}" >> "$TOKEN_PATH"
echo "Serie publicada: ${SER:-N/A}" >> "$TOKEN_PATH"
