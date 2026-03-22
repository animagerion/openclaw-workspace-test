#!/usr/bin/env python3
"""
Script completo de consulta catastral.
1. Busca por dirección usando la API oficial (ovc.catastro.meh.es)
2. Con la referencia catastral, hace scraping de la web de Sedecatastro
3. Combina todos los datos y los presenta de forma estructurada

Uso:
    catastro_full <provincia> <municipio> <calle> [numero]
"""

import sys
import requests
import xmltodict
import re
import argparse
from urllib.parse import quote

BASE_URL = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx"
SEDE_URL = "https://www1.sedecatastro.gob.es"


def consultar_api(provincia, municipio, calle, numero=None, bloque=None, escalera=None, planta=None, puerta=None, sigla=None):
    """Consulta datos via API oficial del Catastro."""
    
    # Primero buscar el tipo de via
    tipo_via = sigla or ''
    nombre_via = calle.upper()
    
    if not sigla:
        params_via = {
            'Provincia': provincia.upper(),
            'Municipio': municipio.upper(),
            'TipoVia': '',
            'NombreVia': nombre_via
        }
        try:
            r = requests.get(f"{BASE_URL}/ConsultaVia", params=params_via, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if r.status_code == 200:
                data = xmltodict.parse(r.content)
                calles = data.get('consulta_callejero', {}).get('callejero', {}).get('calle', [])
                if isinstance(calles, dict):
                    calles = [calles]
                for c in calles:
                    dir_info = c.get('dir', {})
                    nv = dir_info.get('nv', '').upper()
                    if nv and (nv == nombre_via or nombre_via in nv or nv in nombre_via or nombre_via.replace('CL ','').replace('AV ','').replace('PZ ','') in nv):
                        tipo_via = dir_info.get('tv', '')
                        nombre_via = nv
                        break
        except:
            pass
    
    # Consulta principal
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
    
    r = requests.get(f"{BASE_URL}/Consulta_DNPLOC", params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    if r.status_code == 200:
        return xmltodict.parse(r.content)
    return None


def extraer_ref_catastral(datos_api):
    """Extrae la referencia catastral de los datos de la API."""
    try:
        bico = datos_api.get('consulta_dnp', {}).get('bico', {})
        bi = bico.get('bi', {})
        idbi = bi.get('idbi', {})
        rc = idbi.get('rc', {})
        pc1 = rc.get('pc1', '')
        pc2 = rc.get('pc2', '')
        car = rc.get('car', '')
        cc1 = rc.get('cc1', '')
        cc2 = rc.get('cc2', '')
        # Construir RC completa (20 chars)
        rc_completa = f"{pc1}{pc2}{car}{cc1}{cc2}"
        
        # Extraer del/mun codes
        lous = bi.get('dt', {}).get('locs', {}).get('lous', {}).get('lourb', {})
        loin = bi.get('dt', {}).get('loine', {})
        cp = loin.get('cp', '')  # codigo provincia
        cm = loin.get('cm', '')  # codigo municipio
        
        return {
            'rc_completa': rc_completa,
            'pc1': pc1,
            'pc2': pc2,
            'car': car,
            'cc1': cc1,
            'cc2': cc2,
            'del': cp,
            'mun': cm
        }
    except:
        return None


def scraping_sedecatastro(rc_data):
    """Hace scraping de la web de Sedecatastro para obtener datos extra."""
    if not rc_data:
        return None
    
    ref_completa = rc_data['rc_completa']
    del_code = rc_data['del']
    mun_code = rc_data['mun']
    
    # URL de consulta de bien inmueble
    url = f"{SEDE_URL}/CYCBienInmueble/OVCConCiud.aspx?UrbRus=U&RefC={ref_completa}&esBice=&RCBice1=&RCBice2=&DenoBice=&from=OVCBusqueda&pest=rc&RCCompleta={ref_completa}&final=&del={del_code}&mun={mun_code}"
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        html = r.text
        
        datos = {}
        
        # Extraer superficie parcela (superficie gráfica) - busca el patrón con sup
        match = re.search(r'Superficie gráfica.*?<label[^>]*>([\d.,]+)\s*m<sup>2</sup>', html, re.DOTALL)
        if match:
            datos['superficie_parcela'] = match.group(1).replace(',', '.')
        
        # Extraer tabla de construcciones
        construcciones = []
        
        # Buscar la tabla de construcciones
        match_tabla = re.search(r'<table id="ctl00_Contenido_tblLocales"[^>]*>(.*?)</table>', html, re.DOTALL)
        if match_tabla:
            tabla_html = match_tabla.group(1)
            # Buscar todas las filas <tr> dentro de la tabla
            filas = re.findall(r'<tr>(.*?)</tr>', tabla_html, re.DOTALL)
            
            for fila in filas[1:]:  # Saltar la primera (headers)
                # Extraer los <td> de cada fila
                celdas = re.findall(r'<td[^>]*><span>([^<]*)</span></td>', fila)
                if len(celdas) >= 5:
                    # Limpiar espacios
                    celdas = [c.strip() for c in celdas]
                    uso = celdas[0]
                    es = celdas[1].strip()
                    pt = celdas[2].strip()
                    pu = celdas[3].strip()
                    sf = celdas[4].strip()
                    
                    # Saltar si parece ser header
                    if uso in ['Uso principal', ''] or pt == 'Planta':
                        continue
                    
                    construcciones.append({
                        'uso': uso,
                        'escalera': es,
                        'planta': pt,
                        'puerta': pu,
                        'superficie': sf
                    })
        
        if construcciones:
            datos['construcciones'] = construcciones
        
        return datos
        
    except Exception as e:
        return {'error': str(e)}


def formatear_resultado(datos_api, datos_web=None):
    """Formatea el resultado completo."""
    output = []
    output.append("=" * 60)
    output.append("CONSULTA CATASTRAL COMPLETA")
    output.append("=" * 60)
    
    # Datos de la API
    consulta = datos_api.get('consulta_dnp', {})
    bico = consulta.get('bico', {})
    bi = bico.get('bi', {})
    debi = bi.get('debi', {})
    
    # Referencia catastral
    idbi = bi.get('idbi', {})
    rc = idbi.get('rc', {})
    ref_cat = f"{rc.get('pc1', '')}{rc.get('pc2', '')}"
    ref_completa = f"{ref_cat}{rc.get('car', '')}{rc.get('cc1', '')}{rc.get('cc2', '')}"
    
    output.append(f"\n📍 REFERENCIA CATASTRAL: {ref_completa}")
    
    # Localización
    ldt = bi.get('ldt', '')
    output.append(f"\n📌 LOCALIZACIÓN: {ldt}")
    
    # Datos del inmueble
    output.append(f"\n🏠 DATOS DEL INMUEBLE:")
    output.append(f"   Uso: {debi.get('luso', 'N/A')}")
    output.append(f"   Superficie construida: {debi.get('sfc', 'N/A')} m²")
    output.append(f"   Año construcción: {debi.get('ant', 'N/A')}")
    
    # Construcciones de la API
    lcons = bico.get('lcons', {}).get('cons', [])
    if lcons:
        output.append(f"\n📊 DISTRIBUCIÓN (API):")
        if isinstance(lcons, dict):
            lcons = [lcons]
        for cons in lcons:
            tipo = cons.get('lcd', 'N/A')
            stl = cons.get('dfcons', {}).get('stl', 'N/A')
            loint = cons.get('dt', {}).get('lourb', {}).get('loint', {})
            pt = loint.get('pt', '?')
            if pt == '00':
                planta = 'Bajo'
            elif pt.startswith('0'):
                planta = f'Planta {pt.lstrip("0")}'
            else:
                planta = f'Planta {pt}' if pt else '?'
            output.append(f"   - {planta}: {tipo} {stl} m²")
    
    # Datos de la web
    if datos_web:
        output.append(f"\n🌐 DATOS EXTRAIDOS DE SEDECATASTRO.GOB.ES:")
        
        if datos_web.get('superficie_parcela'):
            output.append(f"   Superficie parcela (gráfica): {datos_web['superficie_parcela']} m²")
        
        if datos_web.get('construcciones'):
            output.append(f"\n   📋 CONSTRUCCIONES (web):")
            for cons in datos_web['construcciones']:
                uso = cons.get('uso', '?')
                es = cons.get('escalera', '?')
                pt = cons.get('planta', '?')
                pu = cons.get('puerta', '?')
                sf = cons.get('superficie', '?')
                output.append(f"   - Esc={es}, Pl={pt}, Pu={pu}: {uso} {sf} m²")
    
    output.append("")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='Consulta catastral completa (API + web scraping)')
    parser.add_argument('provincia', help='Provincia (ej: Cadiz, Sevilla)')
    parser.add_argument('municipio', help='Municipio (ej: Rota, Utrera)')
    parser.add_argument('calle', help='Nombre de la calle')
    parser.add_argument('numero', nargs='?', help='Número')
    parser.add_argument('--sigla', '-s', help='Tipo de vía')
    parser.add_argument('--json', '-j', action='store_true', help='Salida JSON')
    
    args = parser.parse_args()
    
    print(f"Consultando: {args.calle} {args.numero or ''}")
    print(f"Municipio: {args.municipio}, {args.provincia}")
    print("...")
    
    # 1. Consulta API
    datos_api = consultar_api(args.provincia, args.municipio, args.calle, args.numero, sigla=args.sigla)
    
    if not datos_api:
        print("Error en la consulta API")
        return 1
    
    # 2. Extraer referencia catastral
    rc_data = extraer_ref_catastral(datos_api)
    if rc_data:
        print(f"Referencia catastral: {rc_data['rc_completa']}")
        
        # 3. Scraping de la web
        print("Extrayendo datos de sedecatastro.gob.es...")
        datos_web = scraping_sedecatastro(rc_data)
        
        # 4. Mostrar resultado
        print(formatear_resultado(datos_api, datos_web))
    else:
        print("No se pudo extraer la referencia catastral")
        print(datos_api)


if __name__ == '__main__':
    main()
