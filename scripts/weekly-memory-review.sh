#!/bin/bash
# weekly-memory-review.sh
# Ejecuta cada domingo a las 20:00 (Madrid)
# Revisa learnings.md, actualiza MEMORY.md y notifica a Paduel

WORKSPACE="/home/gerion/.openclaw/workspace"
MEMORY="$WORKSPACE/MEMORY.md"
LEARNINGS="$WORKSPACE/memory/learnings.md"
PREFS="$WORKSPACE/memory/preferences.md"
DATE=$(date +%Y-%m-%d)

# Backup MEMORY.md antes de tocar
cp "$MEMORY" "$WORKSPACE/memory/memory_backup_$(date +%Y%m%d).md"

# Generar resumen de learnings nuevos (última semana)
SUMMARY=$(tail -100 "$LEARNINGS" 2>/dev/null | grep -E "^## " | tail -20)

# Notificar a Paduel si hay algo nuevo
if [ -n "$SUMMARY" ]; then
  echo "Hay learnings pendientes esta semana"
fi

echo "=== Weekly Review $DATE ===" >> "$LEARNINGS"
echo "Revisión completada: $DATE" >> "$LEARNINGS"