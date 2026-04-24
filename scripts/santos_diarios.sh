#!/usr/bin/env bash
# Santos Diarios — Vatican News + formatting + Telegram send
# Sin LLM, sin timeout, directo

OUTPUT=$(python3 /home/gerion/.openclaw/workspace/scripts/santos_diarios_vatican.py 2>/dev/null)

if [ -n "$OUTPUT" ]; then
    echo "$OUTPUT"
fi
