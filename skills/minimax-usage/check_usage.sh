#!/bin/bash
# MiniMax Token Usage Checker v3
# Consulta el uso del plan MiniMax (por número de llamadas, no tokens)
# 
# Campos de la API:
# - current_interval_total_count: Límite de llamadas por ventana
# - current_interval_usage_count: Llamadas YA USADAS (no disponibles)
# - remains_time: Tiempo restante para reinicio de ventana

AUTH_FILE="/home/gerion/.openclaw/agents/main/agent/auth-profiles.json"

if [ ! -f "$AUTH_FILE" ]; then
    echo "❌ Error: No se encontró el archivo de autenticación"
    exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$AUTH_FILE'))['profiles']['minimax:default']['key'])" 2>/dev/null)

if [ -z "$API_KEY" ]; then
    echo "❌ Error: No se pudo extraer la API key"
    exit 1
fi

RESPONSE=$(curl -s --location "https://platform.minimax.io/v1/api/openplatform/coding_plan/remains" \
  --header "accept: application/json, text/plain, */*" \
  --header "authorization: Bearer $API_KEY" \
  --header "referer: https://platform.minimax.io/user-center/payment/coding-plan" \
  --header "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36" 2>&1)

# Verificar respuesta válida
if ! echo "$RESPONSE" | grep -q "status_code"; then
    echo "❌ Error: Respuesta inválida de la API"
    exit 1
fi

STATUS_CODE=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('base_resp',{}).get('status_code','unknown'))" 2>/dev/null)

if [ "$STATUS_CODE" != "0" ]; then
    STATUS_MSG=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('base_resp',{}).get('status_msg','unknown error'))" 2>/dev/null)
    echo "❌ Error de API: $STATUS_MSG (code: $STATUS_CODE)"
    exit 1
fi

# Guardar response para Python
echo "$RESPONSE" > /tmp/minimax_response.json

python3 << 'PYEOF'
import json
from datetime import datetime

with open('/tmp/minimax_response.json', 'r') as f:
    data = json.load(f)

model = data['model_remains'][0]

# === VENTANA DE 5 HORAS ===
# current_interval_total_count = Límite total de llamadas
# current_interval_usage_count = Llamadas YA usadas (no disponibles)
# remaining = total - usage = Llamadas DISPONIBLES
total_5h = model['current_interval_total_count']
used_5h = model['current_interval_usage_count']
available_5h = total_5h - used_5h
remains_time = model['remains_time']  # Tiempo restante en ms
hours_left = remains_time / 3600000

# Tiempos de ventana
start_time = datetime.fromtimestamp(model['start_time'] / 1000)
end_time = datetime.fromtimestamp(model['end_time'] / 1000)

# Porcentaje usado
pct_used_5h = (used_5h / total_5h) * 100
pct_available_5h = 100 - pct_used_5h

# === SEMANAL ===
total_weekly = model['current_weekly_total_count']
used_weekly = model['current_weekly_usage_count']
available_weekly = total_weekly - used_weekly
pct_used_weekly = (used_weekly / total_weekly) * 100

week_start = datetime.fromtimestamp(model['weekly_start_time'] / 1000)
week_end = datetime.fromtimestamp(model['weekly_end_time'] / 1000)

# === MOSTRAR ===
print("=" * 50)
print("   📊 MINIMAX PLAN - USO DE LLAMADAS")
print("=" * 50)
print()

# Ventana de 5 horas
print("🕐 Ventana de 5 horas (rolling):")
print(f"   Límite:       {total_5h:,} llamadas")
print(f"   Usadas:       {used_5h:,} llamadas ({pct_used_5h:.1f}%)")
print(f"   Disponibles:  {available_5h:,} llamadas ({pct_available_5h:.1f}%)")
print()
print(f"   Inicio:       {start_time.strftime('%d-%m-%Y %H:%M UTC')}")
print(f"   Fin:          {end_time.strftime('%d-%m-%Y %H:%M UTC')}")
print(f"   Tiempo restante: ~{hours_left:.1f} horas")
print()

# Semanal
print("📅 Ventana semanal:")
print(f"   Límite:       {total_weekly:,} llamadas")
print(f"   Usadas:       {used_weekly:,} llamadas ({pct_used_weekly:.1f}%)")
print(f"   Disponibles:  {available_weekly:,} llamadas")
print()
print(f"   Inicio:       {week_start.strftime('%d-%m-%Y %H:%M UTC')}")
print(f"   Fin:          {week_end.strftime('%d-%m-%Y %H:%M UTC')}")
print()
print("=" * 50)

# Alertas ventana 5h
if available_5h < 100:
    print("🚨 CRÍTICO: ¡¡Menos de 100 llamadas disponibles!!")
elif available_5h < 300:
    print("🚨 ALERTA: Llamadas bajas en ventana de 5h")
elif available_5h < 500:
    print("⚠️  AVISO: Pocas llamadas disponibles")
elif pct_used_5h < 50:
    print("✅ Ventana 5h OK")
else:
    print(f"🟡 Ventana 5h: {pct_used_5h:.0f}% usado")

# Alertas semanal
if available_weekly < 100:
    print("🚨 CRÍTICO: ¡¡Menos de 100 llamadas semanales!!")
elif available_weekly < 500:
    print("🚨 ALERTA: Llamadas semanales muy bajas")
elif pct_used_weekly >= 95:
    print("⚠️  AVISO: 95%+ de la semana consumida")
else:
    print(f"✅ Semana OK: {pct_used_weekly:.0f}% usado")

print("=" * 50)
PYEOF

rm -f /tmp/minimax_response.json
