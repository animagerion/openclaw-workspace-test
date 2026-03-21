---
name: catastro
description: Consulta datos catastrales de España por dirección usando la API oficial del Catastro. Genera informe en Google Docs.
---

# Catastro CLI — Datos Catastrales de España

Consulta información catastral de inmuebles usando la **API oficial del Catastro** (ovc.catastro.meh.es).

## Ubicación

CLI: `/home/gerion/.local/bin/catastro` (o `catastro` si ~/.local/bin está en PATH)
Script: `/home/gerion/.openclaw/workspace/scripts/catastro_cli.py`

## Uso del CLI

### Comando básico

```bash
catastro <provincia> <municipio> <calle> [numero]
```

### Ejemplos

```bash
# Consulta básica
catastro Cadiz Rota "Marina" 1
catastro Sevilla Sevilla "Plaza España" 5

# Con tipo de vía específico (opcional)
catastro Cadiz Rota "Marina" 1 --sigla CL
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `<provincia>` | Nombre de la provincia |
| `<municipio>` | Nombre del municipio |
| `<calle>` | Nombre de la calle (sin tipo, ej "Marina", no "CL Marina") |
| `[numero]` | Número del inmueble (opcional pero obligatorio si se especifica) |
| `-s, --sigla` | Tipo de vía: CL (Calle), AV (Avenida), PZ (Plaza), CR (Carretera), etc. |
| `-j, --json` | Salida en JSON |
| `-b, --bloque` | Bloque |
| `-e, --escalera` | Escalera |
| `-p, --planta` | Planta |
| `--puerta` | Puerta |

## API Oficial

Usa los **Servicios Web Libres** del Catastro:
- URL: `https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx/`
- **No requiere certificado ni API key**
- **Gratuito** para datos no protegidos
- Más info: https://www.catastro.hacienda.gob.es/ws/Webservices_Libres.pdf

## Datos que devuelve

- Referencia Catastral
- Dirección completa
- Tipo de alta catastral
- Localización (escalera, planta, puerta)
- Superficie (m²)

## Limitaciones

- **Datos protegidos** (titulares, valor catastral) requieren certificado digital o Cl@ve
- Solo devuelve datos **no protegidos**
- Para datos completos, usar la Sede Electrónica del Catastro con certificado

## Ejemplo de uso con Google Docs

```python
# Generar informe catastral
result = subprocess.run(['catastro', 'Cadiz', 'Rota', 'Marina', '1'], capture_output=True, text=True)
informe = result.stdout

# Subir a Google Docs
gog docs create "Informe Catastral - Rota"
gog docs write <doc_id> --file informe.md --append
gog docs share <doc_id> --email paduel@gmail.com --role reader
```

## Notas

- El CLI determina automáticamente el tipo de vía consultando el callejero
- Si la búsqueda falla, probar con `--sigla CL` (u otro tipo)
- Los datos son de la Dirección General del Catastro (España)
