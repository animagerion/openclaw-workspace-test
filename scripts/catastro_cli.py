#!/usr/bin/env python3
"""
CLI para consultar datos catastrales de España por dirección.
Usa los servicios web oficiales de la Sede Electrónica del Catastro (ovc.catastro.meh.es)

Uso:
    catastro <provincia> <municipio> <calle> [numero]
    catastro Cadiz Rota "Calle Marina" 1
"""

import os
import sys
import argparse
import requests
import xmltodict
import json
from urllib.parse import quote

BASE_URL = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx"


def listar_tipos_via():
    """Lista los tipos de vía disponibles."""
    return {
        'CL': 'Calle',
        'AV': 'Avenida',
        'PZ': 'Plaza',
        'CR': 'Carretera',
        'CS': 'Camino',
        'PS': 'Paseo',
        'GL': 'Glorieta',
        'BO': 'Bloque',
        'UR': 'Urbanización',
        'PQ': 'Parque',
        'JG': 'Jardín',
        'AP': 'Apartamentos',
        'PJ': 'Pasaje',
        'PO': 'Partido',
        'DS': 'Diseminado',
        'SN': 'Sin especificar',
        'NC': 'Sin nombre catastral',
        'VI': 'Vía',
        'RE': 'Residencial',
        'AU': 'Aurora',
        'CI': 'Cinta',
        'CO': 'Cuesta',
        'CY': 'Cañada',
        'CH': 'Chalet',
        'ED': 'Edificio',
        'EN': 'Entrada',
        'ES': 'Estación',
        'FC': 'Ferrocarril',
        'GB': 'Glorieta',
        'HY': 'Huerta',
        'IS': 'Isla',
        'LG': 'Largo',
        'ML': 'Muelle',
        'MZ': 'Manzana',
        'OP': 'Operación',
        'PR': 'Prolongación',
        'PT': 'Portales',
        'RB': 'Rambla',
        'RD': 'Ronda',
        'RZ': 'Raíz',
        'SB': 'Subida',
        'SD': 'Senda',
        'SL': 'Solar',
        'TN': 'Terreno',
        'TR': 'Travesía',
        'VB': 'Variante',
    }


def obtener_tipo_via(provincia, municipio, calle):
    """
    Obtiene el tipo de vía buscando en el callejero.
    Returns dict con tipo_via y nombre_via normalizados.
    """
    params = {
        'Provincia': provincia.upper(),
        'Municipio': municipio.upper(),
        'TipoVia': '',
        'NombreVia': calle.upper() if calle else '',
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    url = f"{BASE_URL}/ConsultaVia"
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        if response.status_code == 200:
            data = xmltodict.parse(response.content, process_namespaces=False)
            return data
    except:
        pass
    return None


def consultar_direccion(provincia, municipio, calle, numero=None, bloque=None, escalera=None, planta=None, puerta=None, sigla=None):
    """
    Consulta datos catastrales por dirección usando la API oficial del Catastro.
    
    Args:
        provincia: Nombre de la provincia (ej: CADIZ, SEVILLA)
        municipio: Nombre del municipio (ej: ROTA, JEREZ)
        calle: Nombre de la calle
        numero: Número del inmueble (opcional)
        bloque, escalera, planta, puerta: Datos adicionales
        sigla: Tipo de vía (ej: CL, AV, PZ). Si no se especifica, se busca automáticamente.
    
    Returns:
        dict con los datos catastrales
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Gerion-CLI/1.0)',
        'Accept': 'application/xml',
    }
    
    # Si no nos dan el tipo de vía, buscar en el callejero
    tipo_via = sigla or ''
    nombre_via = calle.upper()
    
    if not sigla:
        # Buscar la calle para obtener el tipo de vía
        resultado_busqueda = obtener_tipo_via(provincia, municipio, calle)
        if resultado_busqueda:
            try:
                calles = resultado_busqueda.get('consulta_callejero', {}).get('callejero', {}).get('calle', [])
                if isinstance(calles, dict):
                    calles = [calles]
                
                # Buscar coincidencia exacta o parcial
                for c in calles:
                    dir_info = c.get('dir', {})
                    nv = dir_info.get('nv', '').upper()
                    if nv and (nv == nombre_via or nombre_via in nv or nv in nombre_via):
                        tipo_via = dir_info.get('tv', '')
                        nombre_via = nv  # Usar el nombre completo de la calle
                        break
                    # También buscar sin el tipo (ej "MARINA" en "CL MARINA")
                    nombre_simple = nombre_via.replace('CL ', '').replace('AV ', '').replace('PZ ', '').replace('CR ', '')
                    if nombre_simple in nv or nv in nombre_simple:
                        tipo_via = dir_info.get('tv', '')
                        nombre_via = nv  # Usar el nombre completo de la calle
                        break
            except:
                pass
    
    params = {
        'Provincia': provincia.upper(),
        'Municipio': municipio.upper(),
        'Sigla': tipo_via,
        'Calle': nombre_via,
        'Numero': str(numero) if numero else '',
        'Bloque': bloque or '',
        'Escalera': escalera or '',
        'Planta': planta or '',
        'Puerta': puerta or '',
    }
    
    url = f"{BASE_URL}/Consulta_DNPLOC"
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = xmltodict.parse(response.content, process_namespaces=False)
            return data
        else:
            return {'error': f'HTTP {response.status_code}', 'detail': response.text[:500]}
            
    except Exception as e:
        return {'error': str(e)}


def formatear_resultado(datos):
    """Formatea los datos catastrales para mostrar."""
    output = []
    output.append("=" * 60)
    output.append("CONSULTA CATASTRAL POR DIRECCIÓN")
    output.append("=" * 60)
    
    if 'error' in datos:
        output.append(f"\nERROR: {datos['error']}")
        if 'detail' in datos:
            output.append(f"Detalle: {datos['detail']}")
        return "\n".join(output)
    
    consulta = datos.get('consulta_dnp', {})
    control = consulta.get('control', {})
    
    # Handle different response structures
    # Structure 1: Multiple results (lrcdnp.rcdnp)
    # Structure 2: Single result with details (bico.bi)
    resultados = consulta.get('lrcdnp', {}).get('rcdnp', [])
    
    if not resultados:
        # Try alternative structure (bico)
        bico = consulta.get('bico', {})
        if bico:
            bi = bico.get('bi', {})
            if bi:
                resultados = [bi]
        else:
            # Check for error
            lerr = consulta.get('lerr', {})
            if lerr:
                err = lerr.get('err', {})
                if err:
                    output.append(f"\nError del Catastro: {err.get('des', 'Desconocido')}")
                    return "\n".join(output)
    
    if not resultados:
        output.append("\nNo se han encontrado resultados.")
        return "\n".join(output)
    
    num_resultados = control.get('cudnp', len(resultados))
    output.append(f"\n Inmuebles encontrados: {num_resultados}")
    output.append("")
    
    # Handle single result (dict) vs multiple results (list)
    if isinstance(resultados, dict):
        resultados = [resultados]
    
    for i, inmueble in enumerate(resultados, 1):
        # Handle two possible structures: idbi (from bico) and rc (from lrcdnp)
        idbi = inmueble.get('idbi', {})
        rc = idbi.get('rc', {}) if idbi else inmueble.get('rc', {})
        dt = inmueble.get('dt', {})
        debi = inmueble.get('debi', {})
        
        # Reference cadastral
        ref_catastral = f"{rc.get('pc1', '')}{rc.get('pc2', '')}"
        output.append(f"--- Inmueble {i} ---")
        if ref_catastral and ref_catastral != 'None':
            output.append(f"  Referencia Catastral: {ref_catastral}")
        
        # Full address
        ldt = inmueble.get('ldt', '')
        if ldt:
            output.append(f"  Dirección completa: {ldt}")
        else:
            # Build from parts
            nm = dt.get('nm', '')
            np_ = dt.get('np', '')
            locs = dt.get('locs', {})
            
            if isinstance(locs, dict):
                lous = locs.get('lous', {})
                if isinstance(lous, dict):
                    ourb = lous.get('lourb', {})
                    if isinstance(ourb, dict):
                        dir_info = ourb.get('dir', {})
                        tv = dir_info.get('tv', '')
                        nv = dir_info.get('nv', '')
                        pnp = dir_info.get('pnp', '')
                        output.append(f"  Dirección: {tv} {nv}, {pnp}")
        
        # Use type
        if debi:
            uso = debi.get('luso', '')
            if uso:
                output.append(f"  Uso: {uso}")
            sfc = debi.get('sfc', '')
            if sfc:
                output.append(f"  Superficie construida: {sfc} m²")
            ant = debi.get('ant', '')
            if ant:
                output.append(f"  Año construcción: {ant}")
        
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Consulta datos catastrales de España por dirección',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  catastro Cadiz Rota "Calle Marina" 1
  catastro Sevilla Sevilla "Plaza España" 5
  catastro Malaga Malaga "Avenida de la Constitucion" 1

Nota: Usa los servicios web oficiales del Catastro (ovc.catastro.meh.es)
        '''
    )
    
    parser.add_argument('provincia', help='Provincia (ej: Cadiz, Sevilla, Malaga)')
    parser.add_argument('municipio', help='Municipio (ej: Rota, Jerez, Sevilla)')
    parser.add_argument('calle', help='Nombre de la calle')
    parser.add_argument('numero', nargs='?', help='Número de la vivienda')
    parser.add_argument('--bloque', '-b', help='Bloque')
    parser.add_argument('--escalera', '-e', help='Escalera')
    parser.add_argument('--planta', '-p', help='Planta')
    parser.add_argument('--puerta', help='Puerta')
    parser.add_argument('--sigla', '-s', help='Tipo de via (CL, AV, PZ, CR, etc.)')
    parser.add_argument('--json', '-j', action='store_true', help='Salida en JSON')
    
    args = parser.parse_args()
    
    print(f"Consultando: {args.calle} {args.numero or ''}")
    print(f"Municipio: {args.municipio}, {args.provincia}")
    print()
    
    datos = consultar_direccion(
        args.provincia,
        args.municipio,
        args.calle,
        args.numero,
        args.bloque,
        args.escalera,
        args.planta,
        args.puerta,
        args.sigla
    )
    
    if args.json:
        print(json.dumps(datos, indent=2, ensure_ascii=False))
    else:
        print(formatear_resultado(datos))


if __name__ == '__main__':
    main()
