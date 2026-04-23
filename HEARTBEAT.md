# HEARTBEAT.md

## SANTOS_TRIGGER
Cuando llegue un systemEvent con texto "SANTOS_TRIGGER":
1. Ejecutar: bash /home/gerion/.openclaw/workspace/scripts/santos_diarios.sh
2. Si el output no está vacío, enviarlo a Telegram (chat 257331761)
3. Si está vacío, no hacer nada
