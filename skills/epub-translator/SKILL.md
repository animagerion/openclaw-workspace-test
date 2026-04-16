# EPUB Translator Skill

Orquesto la traducción de libros EPUB del inglés al español, capítulo a capítulo, mediante subagentes con doble paso (traducción + revisión). Genero un EPUB final en español.

## LECCIONES CLAVE (de La Última Economía, 2026-04-16)

**EL ERROR CRÍTICO que no repetir:** El EPUB original tiene archivos con nombres crípticos (ej. `68a486d08293a5001c65632a.xhtml`) que NO siguen el orden de lectura. Los archivos del translator se nombran secuencialmente (`translated_chapter_001.txt`, `002.txt`...) pero eso NO corresponde al orden del spine del EPUB.

**Siempre verificar el mapeo contenido por contenido**, no asumir que el número de archivo del translator corresponde al capítulo del EPUB.

El orden de extracción de `parse_epub.py` (usa `ebooklib`) tampoco garantiza ser el mismo que el spine real del EPUB. SIEMPRE verificar con el contenido real.

---

## Flujo de trabajo completo

### 1. Recepción
- Paduel envía el EPUB por Telegram
- Descargo al workspace: `/home/gerion/.openclaw/workspace/skills/epub-translator/`

### 2. Subida a Drive (backup)
- Carpeta: `Libros traducción` (ID: 1VX7jkdnAUDD4QKQyMgVs0-ywn3qnfzlv)
- Guardo el file_id en config.json

### 3. Inicialización
```bash
python3 skills/epub-translator/parse_epub.py <libro.epub> <carpeta_salida>
```
- Extrae capítulos a texto plano en `chapters/chapter_XXX.txt`
- Crea `chapters/chapters_index.json` con metadatos
- **IMPORTANTE:** Anotar el SOURCE_FILE de cada capítulo (nombre real del archivo XHTML en el EPUB)

### 4. Ciclo de traducción
Para cada capítulo, en secuencia:
1. Leer `chapters/chapter_XXX.txt` completo
2. Spawn subagente que traduce al español
3. Spawn segundo subagente que revisa (revisión obligatoria)
4. Guardar en `translated_chapter_XXX.txt`
5. Actualizar `progress.json` (marcar done=true)

### 5. Generación del EPUB final (CRÍTICO)

**NUNCA asumir que `translator_ch005` corresponde al archivo XHTML `chapter_005` del EPUB.**

Pasos:
1. **Verificar mapeo real:** Comparar el primer párrafo del contenido de cada `translated_chapter_XXX.txt` con el primer párrafo del body de cada archivo XHTML del EPUB (extraer con `zipfile + BeautifulSoup`).
2. **Construir el EPUB** reemplazando cada archivo XHTML con su traducción correspondiente según el mapeo verificado.
3. **Actualizar el índice/ToC:** Los archivos `toc.ncx` y `toc.xhtml` contienen los títulos en inglés del índice. Hay que reemplazarlos con los títulos en español correspondientes.
4. **Actualizar metadatos:** Título del libro, idioma en content.opf.

Script de build (usar `zipfile` directamente, NO `ebooklib` que pierde estructura):
```bash
python3 skills/epub-translator/build_epub.py <original.epub> <carpeta> <output.epub>
```

### 6. Verificación post-build
- Abrir el EPUB generado con zipfile y verificar:
  - Que el primer capítulo tenga el contenido correcto
  - Que los títulos del ToC (NCX y XHTML) estén en español
  - Que no haya archivos sin traducir que debieran estar traducidos

### 7. Entrega
- Subir a Drive
- Enviar por Telegram a Paduel

---

## Mapeo Translator → EPUB (código de verificación)

```python
# Para verificar que translator_chXXX va al archivo EPUB correcto:
import zipfile
from bs4 import BeautifulSoup

# Leer primer párrafo del EPUB
with zipfile.ZipFile('libro.epub') as z:
    html = z.read(f'OEBPS/{epub_file}').decode('utf-8')
    s = BeautifulSoup(html, 'html.parser')
    epub_first = s.find('body').find_all('p')[0].get_text()[:60]

# Leer primer párrafo del translator
with open(f'translated_chapter_XXX.txt') as f:
    lines = f.read().split('\n')
    # saltar header (líneas hasta primer blank después de línea 1)
    body_start = 0
    for j, line in enumerate(lines):
        if line.strip() == '' and j > 1:
            body_start = j + 1
            break
    trans_first = '\n'.join(lines[body_start:]).split('\n\n')[0][:60]

# должны совпадать!
print(epub_first)
print(trans_first)
```

## Revisión obligatoria (segundo paso)

El segundo subagente revisa:
- Caracteres chinos, cirílicos o símbolos raros → eliminar
- Texto en inglés sin traducir → traducir
- Español artificial o calcos del inglés → corregir
- Números con formato incorrecto (comas en decimales)
- Acentos faltantes
- Expresiones fuera de contexto

Si hay anomalías graves, se reescribe el capítulo completo.

## Actualización del ToC/Índice

El EPUB tiene dos archivos de índice:
- `OEBPS/toc.ncx` — para lectores EPUB2
- `OEBPS/toc.xhtml` — para lectores EPUB3

Ambos contienen títulos en inglés. Se sustituyen con los títulos en español correspondientes.

```python
# Patrón de sustitución en NCX (navPoint por archivo):
# <text>TÍTULO INGLÉS</text> → <text>TÍTULO ESPAÑOL</text>
# El título está en el último <text> del <navLabel> dentro de cada <navPoint>

# Patrón en XHTML:
# <span>TÍTULO INGLÉS</span> → <span>TÍTULO ESPAÑOL</span>
# Generalmente es el último <span> dentro de cada <a class="toc-entry">
```

## Configuración

- **Carpeta Drive:** `Libros traducción` (ID: 1VX7jkdnAUDD4QKQyMgVs0-ywn3qnfzlv)
- **Carpeta local:** `/home/gerion/.openclaw/workspace/skills/epub-translator/`
- **Credenciales gog:** `GOG_KEYRING_PASSWORD="gerion-gog-2026"`, cuenta `animagerion@gmail.com`

## Comandos de orquestación

```bash
# Inicializar después de subir el EPUB
python3 skills/epub-translator/parse_epub.py <libro.epub> chapters/

# Ver progreso
cat skills/epub-translator/progress.json | python3 -m json.tool

# Traducir capítulo manualmente (si el ciclo automático falla)
# 1. Leer chapter_XXX.txt
# 2. Spawn 2 subagentes (traducción + revisión)
# 3. Guardar en translated_chapter_XXX.txt

# Generar EPUB final (después de traducciones completas)
python3 skills/epub-translator/build_epub.py <original.epub> . <output_ES.epub>

# Subir a Drive
export GOG_KEYRING_PASSWORD="gerion-gog-2026"
gog drive upload <output_ES.epub> --name "<título - ES.epub>"
```

## Reusabilidad

Este skill sirve para CUALQUIER libro en inglés enviado por Telegram.
No está atado a ningún libro concreto. Cada vez que Paduel envíe un EPUB:
1. Lo subo a Drive
2. Actualizo config.json con el file_id
3. Ejecuto parse_epub.py
4. Orkestro capítulo a capítulo
5. **VERIFICO mapeo contenido por contenido antes de build**
6. Genero EPUB y actualizo ToC
