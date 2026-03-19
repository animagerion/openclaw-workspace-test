#!/bin/bash
# MiniMax Token Usage Checker
# Consulta el uso de tokens del plan MiniMax en la ventana de 5 horas

# Obtener API key del archivo de auth de OpenClaw
AUTH_FILE="/home/gerion/.openclaw/agents/main/agent/auth-profiles.json"

if [ ! -f "$AUTH_FILE" ]; then
    echo "❌ Error: No se encontró el archivo de autenticación"
    exit 1
fi

# Extraer API key con Python (más fiable que grep para JSON)
API_KEY=$(python3 -c "import json; print(json.load(open('$AUTH_FILE'))['profiles']['minimax:default']['key'])" 2>/dev/null)

if [ -z "$API_KEY" ]; then
    echo "❌ Error: No se pudo extraer la API key"
    exit 1
fi

# Hacer la llamada a la API
RESPONSE=$(curl -s --location "https://platform.minimax.io/v1/api/openplatform/coding_plan/remains" \
  --header "accept: application/json, text/plain, */*" \
  --header "authorization: Bearer $API_KEY" \
  --header "referer: https://platform.minimax.io/user-center/payment/coding-plan" \
  --header "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" 2>&1)

# Verificar si la respuesta es válida
if echo "$RESPONSE" | grep -q "status_code"; then
    # Extraer el código de estado
    STATUS_CODE=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('base_resp',{}).get('status_code','unknown'))" 2>/dev/null)
    
    if [ "$STATUS_CODE" != "0" ]; then
        STATUS_MSG=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('base_resp',{}).get('status_msg','unknown error'))" 2>/dev/null)
        echo "❌ Error de API: $STATUS_MSG (code: $STATUS_CODE)"
        exit 1
    fi
else
    echo "❌ Error: Respuesta inválida de la API"
    echo "$RESPONSE"
    exit 1
fi

# Parsear y mostrar resultados (tomamos el primer modelo, todos tienen el mismo uso)
echo "=========================================="
echo "   📊 MINIMAX TOKEN PLAN - USO ACTUAL"
echo "=========================================="
echo ""

# Ventana de 5 horas
TOTAL_5H=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['current_interval_total_count'])" 2>/dev/null)
USED_5H=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['current_interval_usage_count'])" 2>/dev/null)
REMAIN_5H=$((TOTAL_5H - USED_5H))
PERCENT_5H=$(python3 -c "print(round($USED_5H * 100 / $TOTAL_5H, 1))")

# Tiempos de ventana
START_MS=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['start_time'])" 2>/dev/null)
END_MS=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['end_time'])" 2>/dev/null)

# Convertir timestamps a fecha legible
START_TIME=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($START_MS/1000).strftime('%d-%m-%Y %H:%M UTC'))")
END_TIME=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($END_MS/1000).strftime('%d-%m-%Y %H:%M UTC'))")

echo "🕐 Ventana de 5 horas (rolling):"
echo "   Límite:  $TOTAL_5H tokens"
echo "   Usado:   $USED_5H tokens"
echo "   Restante: $REMAIN_5H tokens ($PERCENT_5H% usado)"
echo ""
echo "   Inicio ventana: $START_TIME"
echo "   Fin ventana:    $END_TIME"
echo ""

# Ventana semanal
TOTAL_WEEKLY=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['current_weekly_total_count'])" 2>/dev/null)
USED_WEEKLY=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['current_weekly_usage_count'])" 2>/dev/null)
REMAIN_WEEKLY=$((TOTAL_WEEKLY - USED_WEEKLY))
PERCENT_WEEKLY=$(python3 -c "print(round($USED_WEEKLY * 100 / $TOTAL_WEEKLY, 1))")

# Tiempos semanales
WEEK_START_MS=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['weekly_start_time'])" 2>/dev/null)
WEEK_END_MS=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin)['model_remains'][0]['weekly_end_time'])" 2>/dev/null)
WEEK_START=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($WEEK_START_MS/1000).strftime('%d-%m-%Y %H:%M UTC'))")
WEEK_END=$(python3 -c "from datetime import datetime; print(datetime.fromtimestamp($WEEK_END_MS/1000).strftime('%d-%m-%Y %H:%M UTC'))")

echo "📅 Ventana semanal:"
echo "   Límite:  $TOTAL_WEEKLY tokens"
echo "   Usado:   $USED_WEEKLY tokens"
echo "   Restante: $REMAIN_WEEKLY tokens ($PERCENT_WEEKLY% usado)"
echo ""
echo "   Inicio semana: $WEEK_START"
echo "   Fin semana:    $WEEK_END"
echo ""

# Alertas
echo "=========================================="
if [ $REMAIN_5H -lt 100 ]; then
    echo "🚨 ALERTA: ¡Menos de 100 tokens restantes!"
elif [ $REMAIN_5H -lt 300 ]; then
    echo "⚠️  AVISO: Tokens bajos en ventana de 5h"
else
    echo "✅ Tokens OK"
fi

if [ $REMAIN_WEEKLY -lt 500 ]; then
    echo "🚨 ALERTA: ¡Menos de 500 tokens restantes en semana!"
elif [ $REMAIN_WEEKLY -lt 2000 ]; then
    echo "⚠️  AVISO: Tokens semanales bajos"
fi

echo "=========================================="
