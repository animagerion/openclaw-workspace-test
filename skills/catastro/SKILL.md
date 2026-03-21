---
name: catastro
description: Consulta datos catastrales de España por dirección. Genera informe en Google Docs.
---

# Catastro CLI — Datos Catastrales de España

Consulta información catastral de inmuebles usando la dirección.

## Ubicación

CLI: `/home/gerion/.local/bin/catastro` (o `catastro` si ~/.local/bin está en PATH)
Script: `/home/gerion/.openclaw/workspace/scripts/catastro_cli.py`

## API Keys

La API oficial del Catastro (SOAP) es compleja. Recomendamos **catastro-api.es** (API REST):
- Web: https://catastro-api.es/
- Registro gratuito con trial
- API Key necesaria

## Uso del CLI

### Comando básico

```bash
catastro <provincia> <municipio> <calle> [opciones]
```

### Ejemplos

```bash
# Consulta básica
catastro Cadiz Rota "Calle Real"

# Con número
catastro Cadiz Rota "Calle Real" --numero 12

# Completo
catastro Cadiz Rota "Avenida de la Marina" -n 5 -b 1 -e A -p 2

# Salida JSON
catastro Sevilla Sevilla "Plaza España" -n 5 --json
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `-n, --numero` | Número de la vivienda |
| `-b, --bloque` | Bloque o portal |
| `-e, --escalera` | Escalera |
| `-p, --planta` | Planta |
| `--puerta` | Puerta |
| `-j, --json` | Salida en JSON |
| `-k, --komens` | Mostrar comentarios adicionales |

## API Keys

Para usar la API de catastro-api.es:

1. Regístrate en https://catastro-api.es/
2. Obtén tu API Key
3. Configura en TOOLS.md:

```
## Catastro API
- catastro-api.es API Key: <tu-key>
```

## Google Docs

Para generar informe en Google Docs:

```python
# Crear documento con datos catastrales
gog docs create "Informe Catastral - <direccion>"
gog docs write <doc_id> --file <fichero_markdown> --append
gog docs share <doc_id> --email paduel@gmail.com --role reader
```

## Plataformas alternativas

| Plataforma | Notas |
|------------|-------|
| **catastro-api.es** | REST, JSON, API Key, trial gratis |
| **Goolzoom** | API REST para catastral |
| **Oficial (SOAP)** | Compleja, requiere certificado digital |

## Notas

- Sin API Key, el CLI muestra la dirección construida pero no puede consultar datos reales
- Los servicios web oficiales requieren identificación digital (Cl@ve o certificado)
- Algunas consultas están protegidas (datos de titulares requieren autorización)
