#!/bin/bash
# weekly-memory-review.sh
# Ejecuta cada domingo a las 20:00 (Madrid)
# Revisa learnings.md, detecta lagunas comparando con git log,
# actualiza MEMORY.md y notifica a Paduel

WORKSPACE="/home/gerion/.openclaw/workspace"
MEMORY="$WORKSPACE/MEMORY.md"
LEARNINGS="$WORKSPACE/memory/learnings.md"
PREFS="$WORKSPACE/memory/preferences.md"
DATE=$(date +%Y-%m-%d)
WEEK_AGO=$(date -d '7 days ago' +%Y-%m-%d)

# Backup MEMORY.md antes de tocar
cp "$MEMORY" "$WORKSPACE/memory/memory_backup_$(date +%Y%m%d).md"

# --- Detección de lagunas ---
# Commits técnicos de la semana que no tienen aprendizaje documentado
echo "=== Weekly Review $DATE ===" >> "$LEARNINGS"
echo "Revisión completada: $DATE" >> "$LEARNINGS"

# Commits con ficheros de la semana
cd "$WORKSPACE" 2>/dev/null || exit 0

GIT_COMMITS=$(git log --since="$WEEK_AGO" --pretty=format:"%h %s" 2>/dev/null | head -30)
GIT_COUNT=$(echo -n "$GIT_COMMITS" | grep -c . 2>/dev/null || echo 0)

# Entradas reales en learnings (líneas con ### FECHA — TÍTULO)
LEARNING_ENTRIES=$(grep -c "^### " "$LEARNINGS" 2>/dev/null || echo 0)

# Commits modificados en scripts/ y memory/ (técnicos, no triviales)
TECH_COMMITS=$(git log --since="$WEEK_AGO" --pretty=format:"%h %s" -- scripts/ memory/ skills/ 2>/dev/null | head -20)

# Resumen de lo que hay en learnings esta semana
WEEK_LEARNINGS=$(awk -v since="$WEEK_AGO" '
  /^### [0-9]{4}-[0-9]{2}-[0-9]{2}/ {
    # Extraer fecha de la línea
    match($0, /[0-9]{4}-[0-9]{2}-[0-9]{2}/)
    if (RLENGTH > 0) {
      d = substr($0, RSTART, RLENGTH)
      if (d >= since) print "  - " $0
    }
  }
' "$LEARNINGS" 2>/dev/null)

# Reporte
cat <<REPORT

═══════════════════════════════════════════
📋 WEEKLY MEMORY REVIEW — $DATE
═══════════════════════════════════════════

📊 Estadísticas de la semana:
  • Commits totales:        $GIT_COUNT
  • Aprendizajes (total):   $LEARNING_ENTRIES
  • Commits técnicos:       $(echo "$TECH_COMMITS" | grep -c . 2>/dev/null || echo 0)

📚 Aprendizajes capturados esta semana:
${WEEK_LEARNINGS:-  (ninguno)}

🔧 Commits técnicos de la semana (scripts/, memory/, skills/):
${TECH_COMMITS:-  (sin commits técnicos)}

═══════════════════════════════════════════
REPORT

# Si hay commits técnicos sin aprendizaje, marcarlo como lagunas
TECH_COUNT=$(echo -n "$TECH_COMMITS" | grep -c . 2>/dev/null || echo 0)
WEEK_LEARN_COUNT=$(echo -n "$WEEK_LEARNINGS" | grep -c . 2>/dev/null || echo 0)

if [ "$TECH_COUNT" -gt 0 ] && [ "$WEEK_LEARN_COUNT" -eq 0 ]; then
  cat <<GAP
⚠️  LAGUNAS DETECTADAS:
   Hay $TECH_COUNT commits técnicos esta semana pero 0 aprendizajes nuevos.
   Revisa los commits de arriba y captura los aprendizajes con:
     bash $WORKSPACE/scripts/log_learning.sh "Título" -t "..." -w "..." -l "..." -g "tag1 tag2"
GAP
fi

echo "✓ Review guardado en $LEARNINGS"
