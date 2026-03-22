---
name: catastro
description: Consulta datos catastrales de España por dirección. Genera informes y los sube a Google Docs.
---

# Catastro — Datos Catastrales de España

Consulta información catastral de inmuebles usando la API oficial del Catastro (ovc.catastro.meh.es) y scraping de sedecatastro.gob.es. No requiere certificado ni API key.

## Ubicación

- CLI básico: `/home/gerion/.local/bin/catastro` (API, rápido)
- CLI completo: `/home/gerion/.local/bin/catastro_full` (API + web, incluye parcela)
- Scripts: `/home/gerion/.openclaw/workspace/scripts/catastro_cli.py` y `catastro_full.py`

## Dos versiones

### catastro (básico - solo API)
```bash
catastro <provincia> <municipio> <calle> [numero]
```
Consulta rápida vía API oficial.

### catastro_full (completo - API + web scraping + plano)
```bash
catastro_full <provincia> <municipio> <calle> [numero] [opciones]
catastro_full Cadiz Rota "Racillo" 19 --bloque 2 --escalera 5 --planta 3 --puerta A --plano
```
Opciones:
- `--plano` — descarga el plano de la parcela (PNG 120x120px)
- `--bloque`, `-b` — número de bloque
- `--escalera`, `-e` — escalera / portal
- `--planta`, `-p` — planta
- `--puerta`, `-u` — puerta

Extrae de sedecatastro.gob.es:
- Superficie de la parcela (gráfica) ← dato que la API no devuelve
- Construcciones detalladas desde la web
- **Plano de la parcela** (PNG 120x120px) si se usa `--plano`

## Ejemplos

```bash
# Básico (API rápida)
catastro Sevilla Utrera "Forcadell" 8
catastro Cadiz Rota "Marina" 1

# Completo (con parcela)
catastro_full Sevilla Utrera "Gorri" 14
catastro_full Sevilla "Via Marciala" 34

# Con parámetros
catastro Sevilla "Gorri" 14 --sigla CL
```

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

## Limitaciones

- Los datos protegidos (titularidad, valor catastral) requieren certificado digital o Cl@ve
- El scraping web depende de que la estructura HTML no cambie

## Integración con Google Docs

```python
# Generar informe catastral completo
subprocess.run(['catastro_full', 'Sevilla', 'Utrera', 'Forcadell', '8'], capture_output=True, text=True)

# Subir a Google Docs
subprocess.run(['gog', 'docs', 'create', 'Informe Catastral'])
subprocess.run(['gog', 'docs', 'write', '<DOC_ID>', '--file', '/tmp/informe.txt', '--append'])
subprocess.run(['gog', 'docs', 'share', '<DOC_ID>', '--email', 'paduel@gmail.com', '--role', 'reader'])
```
