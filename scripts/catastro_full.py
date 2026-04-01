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
    
    # Consulta principal con todos los parámetros
    params = {
        'Provincia': provincia.upper(),
        'Municipio': municipio.upper(),
        'Sigla': tipo_via,
        'Calle': nombre_via,
        'Numero': str(numero) if numero else '',
        'Bloque': str(bloque) if bloque else '',
        'Escalera': str(escalera) if escalera else '',
        'Planta': str(planta) if planta else '',
        'Puerta': str(puerta) if puerta else '',
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


def scraping_sedecatastro(rc_data, timeout=15):
    """Hace scraping de la web de Sedecatastro para obtener datos extra."""
    if not rc_data:
        return None
    
    ref_completa = rc_data['rc_completa']
    del_code = rc_data['del']
    mun_code = rc_data['mun']
    
    # URL de consulta de bien inmueble
    url = f"{SEDE_URL}/CYCBienInmueble/OVCConCiud.aspx?UrbRus=U&RefC={ref_completa}&esBice=&RCBice1=&RCBice2=&DenoBice=&from=OVCBusqueda&pest=rc&RCCompleta={ref_completa}&final=&del={del_code}&mun={mun_code}"
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=timeout)
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


def descargar_plano_parcela(rc_data, output_path='/tmp/parcela.png'):
    """Descarga el plano de la parcela desde sedecatastro.gob.es.
    
    URL: https://www1.sedecatastro.gob.es/Cartografia/GeneraGraficoParcela.aspx
    Solo funciona a baja resolución (120x120px).
    """
    if not rc_data:
        return None
    
    del_code = rc_data['del']
    mun_code = rc_data['mun']
    # Refcat es pc1 + pc2 (parcela sin sufijos de bien inmueble)
    refcat = f"{rc_data['pc1']}{rc_data['pc2']}"  # 3991007TG5139S
    
    url = f"https://www1.sedecatastro.gob.es/Cartografia/GeneraGraficoParcela.aspx"
    params = {
        'del': del_code,
        'mun': mun_code,
        'refcat': refcat,
        'AnchoPixels': 120,
        'AltoPixels': 120,
    }
    
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code == 200 and 'image' in r.headers.get('content-type', ''):
            with open(output_path, 'wb') as f:
                f.write(r.content)
            return output_path
    except:
        pass
    return None


def descargar_foto_fachada(rc_data, output_path='/tmp/fachada.png'):
    """Descarga la foto de fachada desde sedecatastro.gob.es.
    
    URL: https://www1.sedecatastro.gob.es/Cartografia/FXCC/FotoFachada.aspx
    
    Parámetros:
    - refcat: referencia catastral completa (20 chars)
    - del: código de provincia (2 dígitos)
    - mun: código de municipio (3 dígitos) - el código de la API puede diferir del usado en sedecatastro web
    - from: origen (OVCListaBienes)
    - captcha: token CSRF generado dinámicamente en la sesión
    
    El sitio puede bloquear peticiones desde ciertas IPs o requerir captcha.
    """
    if not rc_data:
        return None
    
    del_code = rc_data['del']
    mun_code = rc_data['mun']
    ref_completa = rc_data['rc_completa']  # 20 chars
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www1.sedecatastro.gob.es/',
    })
    
    try:
        # Paso 1: visitar la página principal para establecer sesión
        session.get("https://www1.sedecatastro.gob.es/", timeout=10)
    except:
        pass
    
    # Paso 2: intentar obtener la imagen de fachada
    # El captcha se genera dinámicamente en la página de OVCListaBienes
    # Primero probamos sin captcha (a veces funciona si la IP no está bloqueada)
    facade_url = (
        f"https://www1.sedecatastro.gob.es/Cartografia/FXCC/FotoFachada.aspx"
        f"?refcat={ref_completa}&del={del_code}&mun={mun_code}&from=OVCListaBienes"
    )
    
    try:
        r = session.get(facade_url, timeout=15)
        if r.status_code == 200 and 'image' in r.headers.get('content-type', '') and len(r.content) > 1000:
            with open(output_path, 'wb') as f:
                f.write(r.content)
            return output_path
    except:
        pass
    
    # Paso 3: si no funciona, intentar con mun_code diferente
    # El código de municipio en sedecatastro.gob.es puede diferir del de la API
    # Intentar con códigos comunes alternativamente
    alt_mun_codes = ['42', '069', '00', '01']
    for alt_mun in alt_mun_codes:
        if alt_mun == mun_code:
            continue
        facade_url_alt = (
            f"https://www1.sedecatastro.gob.es/Cartografia/FXCC/FotoFachada.aspx"
            f"?refcat={ref_completa}&del={del_code}&mun={alt_mun}&from=OVCListaBienes"
        )
        try:
            r = session.get(facade_url_alt, timeout=15)
            if r.status_code == 200 and 'image' in r.headers.get('content-type', '') and len(r.content) > 1000:
                with open(output_path, 'wb') as f:
                    f.write(r.content)
                return output_path
        except:
            pass
    
    return None


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
    
    # Superficie parcela (de web)
    if datos_web and datos_web.get('superficie_parcela'):
        output.append(f"   Superficie parcela: {datos_web['superficie_parcela']} m²")
    
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
    parser.add_argument('--bloque', '-b', help='Bloque')
    parser.add_argument('--escalera', '-e', help='Escalera / Portal')
    parser.add_argument('--planta', help='Planta')
    parser.add_argument('--puerta', '-u', help='Puerta')
    parser.add_argument('--json', '-j', action='store_true', help='Salida JSON')
    parser.add_argument('--plano', action='store_true', default=True, help='Descarga el plano de la parcela (por defecto True)')
    parser.add_argument('--pdf', action='store_true', help='Genera un informe PDF profesional')
    parser.add_argument('--basic', action='store_true', help='Solo consulta API rápida, sin web scraping ni plano')
    
    args = parser.parse_args()
    
    print(f"Consultando: {args.calle} {args.numero or ''}")
    print(f"Municipio: {args.municipio}, {args.provincia}")
    print("...")
    
    # 1. Consulta API
    datos_api = consultar_api(args.provincia, args.municipio, args.calle, args.numero, 
                             bloque=args.bloque, escalera=args.escalera, 
                             planta=args.planta, puerta=args.puerta, sigla=args.sigla)
    
    if not datos_api:
        print("Error en la consulta API")
        return 1
    
    # 2. Extraer referencia catastral
    rc_data = extraer_ref_catastral(datos_api)
    if rc_data:
        print(f"Referencia catastral: {rc_data['rc_completa']}")
        
        # 3. Scraping de la web (skip if --basic)
        datos_web = None
        if not args.basic:
            print("Extrayendo datos de sedecatastro.gob.es...")
            datos_web = scraping_sedecatastro(rc_data)
        
        # 4. Descargar plano si se pide (skip if --basic)
        plano_path = None
        if args.plano and not args.basic:
            print("Descargando plano de la parcela...")
            plano_path = descargar_plano_parcela(rc_data)
            if plano_path:
                # Copiar a workspace para poder enviar por Telegram
                import shutil
                import os
                workspace_path = os.path.expanduser('~/.openclaw/workspace/parcela_catastro.png')
                shutil.copy(plano_path, workspace_path)
                print(f"Plano descargado: {workspace_path}")
            else:
                print("No se pudo descargar el plano")
        
        # 5. Descargar foto de fachada si se pide (skip if --basic)
        fachada_path = None
        if not args.basic:
            print("Descargando foto de fachada...")
            fachada_path = descargar_foto_fachada(rc_data)
            if fachada_path:
                import shutil
                import os
                workspace_path = os.path.expanduser('~/.openclaw/workspace/fachada_catastro.png')
                shutil.copy(fachada_path, workspace_path)
                print(f"Foto de fachada descargada: {workspace_path}")
            else:
                print("No se pudo descargar la foto de fachada (puede que no exista o el sitio esté bloqueado)")
        
        # 6. Generar PDF si se pide
        pdf_path = None
        if args.pdf:
            print("Generando informe PDF...")
            import shutil as sh
            import os
            # Importar el generador de informes
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            try:
                from catastro_report import generar_informe_catastral
                pdf_output = os.path.expanduser(f'~/.openclaw/workspace/informe_catastral.pdf')
                plano_for_pdf = os.path.expanduser('~/.openclaw/workspace/parcela_catastro.png') if args.plano and plano_path else None
                generar_informe_catastral(
                    datos_api=datos_api,
                    datos_web=datos_web,
                    output_path=pdf_output,
                    plano_path=plano_for_pdf,
                    satelite_path=None,
                )
                pdf_path = pdf_output
                print(f"Informe PDF generado: {pdf_path}")
            except Exception as e:
                print(f"Error generando PDF: {e}")
        
        # 7. Mostrar resultado
        print(formatear_resultado(datos_api, datos_web))
    else:
        print("No se pudo extraer la referencia catastral")
        print(datos_api)


if __name__ == '__main__':
    main()
