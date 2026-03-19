---
name: minimax-usage
description: Consulta el uso de tokens del plan MiniMax en la ventana de 5 horas. Ejecuta el script de consulta y muestra los resultados de forma clara.
---

# MiniMax Token Usage

Usa el CLI `minimax-usage` para consultar el consumo actual de tokens.

## Uso

Ejecuta el script directamente:

```bash
/home/gerion/.openclaw/workspace/skills/minimax-usage/check_usage.sh
```

## Script

El script consulta la API de MiniMax:

```bash
curl -s --location "https://platform.minimax.io/v1/api/openplatform/coding_plan/remains" \
  --header "accept: application/json, text/plain, */*" \
  --header "authorization: Bearer <API_KEY>" \
  --header "referer: https://platform.minimax.io/user-center/payment/coding-plan" \
  --header "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
```

La API key se obtiene automáticamente del archivo `auth-profiles.json` de OpenClaw.

## Interpretación de resultados

- **current_interval_total_count**: Límite de tokens en la ventana de 5 horas
- **current_interval_usage_count**: Tokens ya consumidos en la ventana actual
- **remaining**: Tokens restantes (límite - usado)
- **weekly_*** : Estadísticas semanales

## Ejemplo de respuesta parseada

El script muestra:
- Ventana de 5h: X/Y tokens (Z restantes)
- Ventana semanal: X/Y tokens (Z restantes)
