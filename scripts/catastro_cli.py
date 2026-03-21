#!/usr/bin/env python3
"""
CLI para consultar datos catastrales de España por dirección.
Usa los servicios web oficiales de la Sede Electrónica del Catastro.

Uso:
    catastro <direccion> [provincia]
    catastro "Calle Real 12" Cadiz
    catastro "Plaza España 5" "Sevilla"
"""

import os
import sys
import argparse
import requests
import json
from urllib.parse import quote

BASE_URL = "https://www.sedecatastro.gob.es"

def buscar_callejero(provincia, municipio, calle=None, numero=None):
    """
    Busca en el callejero catastral.
    Returns dict con información de parcelas encontradas.
    """
    params = {
        'provincia': provincia.upper(),
        'municipio': municipio.upper(),
    }
    if calle:
        params['calle'] = calle
    if numero:
        params['numero'] = numero
    
    url = f"{BASE_URL}/calie/cyc/buscar/"
    # This is a simplified approach - the actual API has complex SOAP/REST endpoints
    
    # Use the public CPV (Callejero de Pendientes Virtual)
    # Alternative: use the direct webservice
    return params

def consultar_por_direccion(direccion, provincia=None, municipio=None):
    """
    Consulta datos catastrales usando la dirección proporcionada.
    Usa el servicio de coordenadas y reference catastral.
    """
    # Clean address
    direccion = direccion.strip()
    
    # Build query - try the simple search endpoint first
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Gerion-CLI/1.0)',
        'Accept': 'application/json, text/plain, */*',
    }
    
    # Method 1: Use the SEC18 endpoint for address search
    url = f"{BASE_URL}/SEC18/AccSecuenciaCriteriosBusqueda/BDCO/Portals/Paginas_Seccions/Descarga/ApartadoDescargas.aspx"
    
    # Method 2: Use the actual REST endpoint
    # The catastro API uses a complex SOAP-based system
    # For simplicity, we'll use a direct HTTP approach
    
    return None

def consultar_rc(referencia_catastral):
    """
    Consulta datos de una parcela por su referencia catastral.
    """
    # This would use the actual RC (Reference Catastral)
    pass

def formatear_resultado(datos):
    """Formatea los datos catastrales para mostrar."""
    output = []
    output.append("=" * 60)
    output.append("DATOS CATASTRALES")
    output.append("=" * 60)
    
    if not datos:
        return "\n".join(output) + "\n\nNo se han encontrado datos. Verifica la dirección."
    
    for key, value in datos.items():
        if isinstance(value, dict):
            output.append(f"\n{key}:")
            for k, v in value.items():
                output.append(f"  - {k}: {v}")
        else:
            output.append(f"{key}: {value}")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Consulta datos catastrales de España por dirección',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  catastro "Calle Real 12" Cadiz Rota
  catastro "Plaza España 5" Sevilla
  catastro "Avenida de la Constitucion 1" Malaga

Nota: Se necesita conexion a internet para consultar el catastro.
        '''
    )
    
    # Use nargs='+' for address parts so we can handle multi-word addresses
    parser.add_argument('provincia', help='Provincia (ej: Cadiz, Sevilla, Malaga)')
    parser.add_argument('municipio', help='Municipio (ej: Rota, Jerez, Sevilla)')
    parser.add_argument('calle', help='Nombre de la calle')
    parser.add_argument('--numero', '-n', help='Número de la vivienda (opcional)')
    parser.add_argument('--bloque', '-b', help='Bloque o portal (opcional)')
    parser.add_argument('--escalera', '-e', help='Escalera (opcional)')
    parser.add_argument('--planta', '-p', help='Planta (opcional)')
    parser.add_argument('--puerta', help='Puerta (opcional)')
    parser.add_argument('--komens', '-k', action='store_true', help='Muestra más detalles')
    parser.add_argument('--json', '-j', action='store_true', help='Salida en JSON')
    
    args = parser.parse_args()
    
    # Build the address for query
    direccion_parts = [args.calle]
    if args.numero:
        direccion_parts.append(f" {args.numero}")
    if args.bloque:
        direccion_parts.append(f" Bloque {args.bloque}")
    if args.escalera:
        direccion_parts.append(f" Esc {args.escalera}")
    if args.planta:
        direccion_parts.append(f" {args.planta}")
    if args.puerta:
        direccion_parts.append(f" {args.puerta}")
    
    direccion = "".join(direccion_parts).strip()
    
    print(f"Buscando: {direccion}")
    print(f"Municipio: {args.municipio}, {args.provincia}")
    print()
    
    # Try the catastro search API
    result = buscar_direccion_catastro(args.provincia, args.municipio, direccion)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(formatear_resultado(result))


def buscar_direccion_catastro(provincia, municipio, direccion):
    """
    Busca una dirección en el catastro usando los servicios web.
    """
    try:
        # Build the query for the catastro CPV (Callejero de Predios Virtual)
        # URL encoding for the address
        prov = provincia.upper()
        mun = municipio.upper()
        cal = direccion.upper()
        
        # The official endpoint uses a complex form-based search
        # Let's try the REST-like endpoint
        url = f"https://www.sedecatastro.gob.es/ACCESIBILIDAD/WS/BuscarCatastro.asmx/Provincia"
        
        # Try the actual CPV search endpoint
        # Based on the official documentation
        params = {
            'Provincia': prov,
            'Municipio': mun,
            'NombreVia': cal,
        }
        
        # Try the CPV service
        try:
            response = requests.get(
                "https://www.catastro.hacienda.gob.es/ws/rest/servicios/callejero",
                params=params,
                headers={
                    'Accept': 'application/json',
                    'User-Agent': 'Gerion-CLI/1.0'
                },
                timeout=15
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data
                except:
                    # Try XML
                    return {'raw': response.text[:1000]}
        except Exception as e:
            pass
        
        # Fallback: return basic info about what we searched
        return {
            'provincia': prov,
            'municipio': mun,
            'direccion_buscada': cal,
            'nota': 'API directa no disponible. Usar la web del catastro para verificar.',
            'enlace': f'https://www.sedecatastro.gob.es/calie/cyc/buscar/?provincia={quote(prov)}&municipio={quote(mun)}&calle={quote(cal)}'
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'provincia': provincia,
            'municipio': municipio,
            'direccion': direccion
        }


if __name__ == '__main__':
    main()
