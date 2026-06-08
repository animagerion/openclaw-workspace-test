#!/bin/bash
# log_learning.sh
# Añade una entrada a memory/learnings.md con formato consistente.
# Uso: log_learning.sh "Título" -t "Tarea hecha" -w "Qué pasó" -l "Lección" -g "tag1 tag2"
#      log_learning.sh "Título" --task "..." --what "..." --learned "..." --tags "..."

set -e

WORKSPACE="/home/gerion/.openclaw/workspace"
LEARNINGS="$WORKSPACE/memory/learnings.md"
DATE=$(date +%Y-%m-%d)

TITLE=""
TASK=""
WHAT=""
LEARNED=""
TAGS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--task) TASK="$2"; shift 2 ;;
    -w|--what) WHAT="$2"; shift 2 ;;
    -l|--learned) LEARNED="$2"; shift 2 ;;
    -g|--tags) TAGS="$2"; shift 2 ;;
    -h|--help)
      cat <<EOF
Uso: log_learning.sh "Título" [opciones]

Opciones:
  -t, --task      Qué tarea se hizo (1 línea)
  -w, --what      Qué pasó (1-3 frases)
  -l, --learned   Lección concreta (1-2 frases)
  -g, --tags      Tags separados por espacio (ej: "openclaw debug")
  -h, --help      Esta ayuda
EOF
      exit 0
      ;;
    -*) echo "Opción desconocida: $1" >&2; exit 1 ;;
    *) TITLE="$1"; shift ;;
  esac
done

if [ -z "$TITLE" ]; then
  echo "Error: título obligatorio" >&2
  exit 1
fi

# Crear archivo si no existe
[ -f "$LEARNINGS" ] || touch "$LEARNINGS"

# Evitar duplicado exacto del mismo día
if grep -q "^### $DATE — $TITLE" "$LEARNINGS" 2>/dev/null; then
  echo "Ya existe una entrada con ese título hoy. No añado duplicado." >&2
  exit 1
fi

# Insertar la entrada justo después de la línea "## Entradas"
TMP=$(mktemp)
awk -v title="$TITLE" -v date="$DATE" -v task="$TASK" -v what="$WHAT" -v learned="$LEARNED" -v tags="$TAGS" '
/^## Entradas/ {
  print $0
  print ""
  print "### " date " — " title
  if (task != "") print "- **Tarea:** " task
  if (what != "") print "- **Qué pasó:** " what
  if (learned != "") print "- **Lección:** " learned
  if (tags != "") print "- **Tags:** " tags
  print ""
  next
}
{ print }
' "$LEARNINGS" > "$TMP"
mv "$TMP" "$LEARNINGS"

echo "OK: entrada añadida a $LEARNINGS"
echo "  Título: $TITLE"
echo "  Tags:   ${TAGS:-<ninguno>}"
