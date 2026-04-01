---
name: catastro
description: Consulta datos catastrales de España por dirección. Genera informes y los sube a Google Docs.
---

# Catastro — Datos Catastrales de España

**Siempre que el usuario pida una consulta catastral, seguir esta secuencia completa:**

1. Ejecutar `catastro_full` con la dirección proporcionada (con `--pdf` para generar informe)
2. Mostrar todos los datos catastrales obtenidos (ref. catastral, dirección, uso, superficie construida, año construcción, distribución por plantas, superficie de la parcela)
3. Enviar el **plano de la parcela** (ya lo descarga `catastro_full`)
4. **Intentar descargar la foto de fachada** (ver sección dedicada más abajo)
5. Si se usó `--pdf`, enviar también el **PDF generado** por Telegram
6. Enviar la foto de fachada si se obtuvo correctamente

**Nunca** enviar solo los datos en texto. Siempre incluir plano y, si se puede, el PDF.

## Ubicación

- CLI básico: `/home/gerion/.local/bin/catastro` (API, rápido)
- CLI completo: `/home/gerion/.local/bin/catastro_full` (API + web, incluye parcela y plano)
- Scripts: `/home/gerion/.openclaw/workspace/scripts/catastro_cli.py`, `catastro_full.py` y `catastro_report.py`
- Generador PDF: `catastro_report.py` — genera informes PDF profesionales con ReportLab

## Uso estándar

```bash
# Ejecutar catastro_full y mostrar resultado (con PDF)
catastro_full <provincia> <municipio> <calle> [numero] --pdf

# Ejemplo
catastro_full SEVILLA Utrera "Donaires" 8 --pdf
catastro_full CORDOBA Montilla "Juan Colin" 29 --pdf
```

**Nota:** Provincia "Córdoba" debe pasarse como `CORDOBA` (sin acento) para evitar error 500 en la API.

## Dos versiones

### catastro (básico - solo API)
```bash
catastro <provincia> <municipio> <calle> [numero]
```
Consulta rápida vía API oficial.

### catastro_full (completo - API + web scraping + plano)
```bash
catastro_full <provincia> <municipio> <calle> [numero] [opciones]
```
Descarga automáticamente el plano de la parcela a:
`/home/gerion/.openclaw/workspace/parcela_catastro.png`

Opciones:
- `--plano` — descarga el plano de la parcela (PNG 120x120px)
- `--pdf` — genera un informe PDF profesional con todos los datos
- `--bloque`, `-b` — número de bloque
- `--escalera`, `-e` — escalera / portal
- `--planta`, `-p` — planta
- `--puerta`, `-u` — puerta

## Foto de fachada

Sedecatastro.gob.es puede tener una foto de fachada para algunos inmuebles.

**Endpoint:** `https://www1.sedecatastro.gob.es/Cartografia/FXCC/FotoFachada.aspx?refc=<REF>&del=<DEL>&mun=<MUN>`

Necesita sesión con cookies de la página principal. Para descargarla:

```python
import requests

refc = "5613526UG5651S0001GO"  # Referencia catastral completa
del_code = "14"  # Códigoprovincia (2 dígitos)
mun_code = "069"  # Código municipio (3 dígitos)

s = requests.Session()
s.get(f"https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCConCiud.aspx?UrbRus=U&RefC={refc}&del={del_code}&mun={mun_code}", headers={'User-Agent': 'Mozilla/5.0'})
r = s.get(f"https://www1.sedecatastro.gob.es/Cartografia/FXCC/FotoFachada.aspx?refc={refc}&del={del_code}&mun={mun_code}", headers={'User-Agent': 'Mozilla/5.0'})
if r.status_code == 200 and len(r.content) > 100:
    with open('/tmp/fachada.png', 'wb') as f:
        f.write(r.content)
```

**Limitaciones de la foto de fachada:**
- No todos los inmuebles tienen foto disponible
- El endpoint puede devolver contenido vacío (0 bytes)
- Si falla, no bloquear la consulta — continuar sin la foto

## Valoración Inmobiliaria (estimación de precio)

Script: `/home/gerion/.openclaw/workspace/scripts/valuation_scraper.py`

Usa Idealista para obtener precio €/m² de una zona y lo multiplica por la superficie construida (catastral).

```bash
# Por dirección
python3 valuation_scraper.py "Calle Donaires 8, Utrera" 348

# Por coordenadas
python3 valuation_scraper.py --lat 37.1852 --lon -5.7799 150

# Por código postal
python3 valuation_scraper.py --postal 41710 200
```

**Funcionamiento:**
1. Intenta hacer scraping de Idealista.es para obtener precio €/m² en la zona
2. Si Idealista bloquea (DataDome), usa media INE regional por provincia como fallback
3. Calcula: valor = precio/m² × superficie
4. Devuelve rango: conservador (−10%%), media, optimista (+10%%)

**Fallback (cuando Idealista bloquea):** Usa tabla de precios medios por provincia/municipio basados en datos INE 2024-2025.

**Cache:** Los resultados se guardan en `/tmp/idealista_cache.json` para evitar re-scraping.

## Datos que devuelve

| Dato | Fuente |
|------|--------|
| Referencia Catastral (20 chars) | API |
| Dirección completa | API |
| Uso (Residencial, etc.) | API |
| Superficie construida total | API |
| Año de construcción | API |
| Distribución por plantas | API |
| **Superficie de la parcela** | Web scraping ← |
| Construcciones detalladas | Web scraping |
| **Plano de la parcela** | Web scraping (PNG) |
| **Foto de fachada** | Web scraping (si disponible) |
| **Informe PDF** | Generado con ReportLab (con `--pdf`) |

## Integración con Google Docs

```python
# Generar informe catastral completo
subprocess.run(['catastro_full', 'Sevilla', 'Utrera', 'Forcadell', '8'], capture_output=True, text=True)

# Subir a Google Docs
subprocess.run(['gog', 'docs', 'create', 'Informe Catastral'])
subprocess.run(['gog', 'docs', 'write', '<DOC_ID>', '--file', '/tmp/informe.txt', '--append'])
subprocess.run(['gog', 'docs', 'share', '<DOC_ID>', '--email', 'paduel@gmail.com', '--role', 'reader'])
```
