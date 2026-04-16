# EPUB Translator Skill

Orquesto la traducción de libros EPUB del inglés al español, capítulo a capítulo, mediante subagentes con doble paso (traducción + revisión). Genero un EPUB final en español.

## Flujo de trabajo

### 1. Paduel me envía el EPUB por Telegram
- El archivo llega como documento/mensaje de Telegram
- Lo descargo al workspace o a /tmp/

### 2. Subo a Google Drive
- Carpeta destino: `Libros traducción` (ID: 1VX7jkdnAUDD4QKQyMgVs0-ywn3qnfzlv)
- Guardo el file_id en config.json

### 3. Inicializo
- Extraigo los capítulos con `parse_epub.py`
- Creo `progress.json` con el índice de capítulos

### 4. Ciclo de traducción
Para cada capítulo (capítulo a capítulo, no en paralelo):
1. Spawneo subagente que traduce al español (MiniMax)
2. Spawneo segundo subagente que revisa y corrige
3. Guardo traducción en la carpeta chapters/
4. Actualizo progress.json

### 5. Genero EPUB final
- Reconstruyo el EPUB con `build_epub.py`
- Lo subo a Drive en `Libros traducción`
- Notifico a Paduel por Telegram

## Comandos de orquestación

```bash
# Inicializar después de subir el EPUB
python3 skills/epub-translator/coordinator.py --init

# Ver progreso
python3 skills/epub-translator/coordinator.py --status

# Traducir siguiente capítulo (manual)
python3 skills/epub-translator/coordinator.py --next

# Generar EPUB final
python3 skills/epub-translator/coordinator.py --build
```

## Revisión obrigatória (segundo paso)

Después de cada traducción, el segundo subagente revisa:
- Caracteres chinos, cirílicos, o símbolos raros → eliminar
- Texto en inglés sin traducir → traducir
- Español artificial o calcos del inglés → corregir
- Números con formato incorrecto (comas en decimales)
- Acentos faltantes
- Expresiones extrañas o fuera de contexto

Si hay anomalías graves, se reescribe el capítulo completo.

## Configuración

Carpeta Drive: `Libros traducción` (ID fijo: 1VX7jkdnAUDD4QKQyMgVs0-ywn3qnfzlv)
Carpeta local: `/home/gerion/.openclaw/workspace/skills/epub-translator/chapters/`

## Reusabilidad

Este skill sirve para CUALQUIER libro en inglés enviado por Telegram.
No está atado a ningún libro concreto. Cada vez que Paduel envíe un EPUB:
1. Lo subo a Drive
2. Actualizo config.json con el file_id
3. Ejecuto --init
4. Orkestro capítulo a capítulo