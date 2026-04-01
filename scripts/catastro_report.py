#!/usr/bin/env python3
"""
Generador de informes catastrales en PDF.

Genera un PDF profesional con los datos completos de un inmueble:
- Datos identificativos (ref. catastral, dirección)
- Datos físicos (superficie, año, uso)
- Distribución por plantas
- Plano de la parcela
- Mapa satélite (si se proporciona)
- Datos de construcciones

Uso:
    from catastro_report import generar_informe_catastral
    generar_informe_catastral(datos_api, datos_web, output_path, plano_path=None, satelite_path=None)

O desde línea de comandos:
    python3 catastro_report.py <provincia> <municipio> <calle> <numero>
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ─── Colores del informe ───────────────────────────────────────────
COLOR_HEADER_BG = HexColor("#1a3a5c")   # Azul oscuro institucional
COLOR_HEADER_TEXT = white
COLOR_SUBHEADER_BG = HexColor("#f77002")  # Naranja catastro
COLOR_SUBHEADER_TEXT = white
COLOR_ALT_ROW = HexColor("#f5f5f5")
COLOR_BORDER = HexColor("#cccccc")
COLOR_TEXT = HexColor("#333333")
COLOR_MUTED = HexColor("#666666")


# ─── Estilos ───────────────────────────────────────────────────────
def get_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles['title'] = ParagraphStyle(
        'title',
        fontSize=18,
        fontName='Helvetica-Bold',
        textColor=COLOR_HEADER_TEXT,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles['subtitle'] = ParagraphStyle(
        'subtitle',
        fontSize=10,
        fontName='Helvetica',
        textColor=COLOR_HEADER_TEXT,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    styles['section_header'] = ParagraphStyle(
        'section_header',
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=COLOR_SUBHEADER_TEXT,
        spaceBefore=8,
        spaceAfter=4,
        leftIndent=4,
    )
    styles['label'] = ParagraphStyle(
        'label',
        fontSize=9,
        fontName='Helvetica-Bold',
        textColor=COLOR_MUTED,
        spaceBefore=4,
    )
    styles['value'] = ParagraphStyle(
        'value',
        fontSize=10,
        fontName='Helvetica',
        textColor=COLOR_TEXT,
        spaceBefore=0,
    )
    styles['value_large'] = ParagraphStyle(
        'value_large',
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=COLOR_TEXT,
        spaceBefore=0,
    )
    styles['footer'] = ParagraphStyle(
        'footer',
        fontSize=7,
        fontName='Helvetica',
        textColor=COLOR_MUTED,
        alignment=TA_CENTER,
    )
    styles['small'] = ParagraphStyle(
        'small',
        fontSize=8,
        fontName='Helvetica',
        textColor=COLOR_MUTED,
        alignment=TA_CENTER,
    )

    return styles


# ─── Helper: header banner ─────────────────────────────────────────
class HeaderBanner(canvas.Canvas):
    """Canvas auxiliar para dibujar la cabecera en cada página."""

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header(self):
        w, h = A4
        # Barra azul
        self.setFillColor(COLOR_HEADER_BG)
        self.rect(0, h - 1.8*cm, w, 1.8*cm, fill=1, stroke=0)
        # Título
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 14)
        self.drawString(1*cm, h - 1.2*cm, "INFORME CATASTRAL")
        self.setFont('Helvetica', 9)
        self.drawRightString(w - 1*cm, h - 1.0*cm, "Sede Electrónica del Catastro")
        self.setFont('Helvetica', 8)
        self.drawString(1*cm, h - 1.55*cm, "Datos no oficiales — solo con carácter informativo")
        # Pie de página
        page_num = self._pageNumber
        self.setFillColor(COLOR_MUTED)
        self.setFont('Helvetica', 7)
        self.drawCentredString(w / 2, 0.7*cm, f"Página {page_num}  |  Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")


# ─── Generador principal ──────────────────────────────────────────
def generar_informe_catastral(
    datos_api: dict,
    datos_web: dict = None,
    output_path: str = "/tmp/informe_catastral.pdf",
    plano_path: str = None,
    satelite_path: str = None,
) -> str:
    """
    Genera un PDF con los datos catastrales del inmueble.

    Args:
        datos_api:    Datos devueltos por la API del Catastro.
        datos_web:    Datos extraídos de sedecatastro.gob.es (superficie parcela, etc.).
        output_path:  Ruta donde guardar el PDF.
        plano_path:   Ruta a la imagen del plano de la parcela.
        satelite_path: Ruta a la imagen de satélite del inmueble.

    Returns:
        Ruta del PDF generado.
    """

    # ── Extraer datos de la API ────────────────────────────────────
    consulta = datos_api.get('consulta_dnp', {})
    bico = consulta.get('bico', {})
    bi = bico.get('bi', {})
    debi = bi.get('debi', {})
    idbi = bi.get('idbi', {})
    rc = idbi.get('rc', {})

    ref_completa = (
        f"{rc.get('pc1', '')}{rc.get('pc2', '')}"
        f"{rc.get('car', '')}{rc.get('cc1', '')}{rc.get('cc2', '')}"
    )
    ref_parcela = f"{rc.get('pc1', '')}{rc.get('pc2', '')}"
    ldt = bi.get('ldt', '')          # dirección completa
    uso = debi.get('luso', 'N/A')
    sfc = debi.get('sfc', 'N/A')     # superficie construida
    ant = debi.get('ant', 'N/A')      # año construcción

    # Superficie parcela (de web)
    sup_parcela = None
    if datos_web and datos_web.get('superficie_parcela'):
        sup_parcela = datos_web['superficie_parcela']

    # Construcciones
    lcons = bico.get('lcons', {}).get('cons', [])
    if isinstance(lcons, dict):
        lcons = [lcons]

    constructions = []
    for cons in lcons:
        tipo = cons.get('lcd', '?')
        stl = cons.get('dfcons', {}).get('stl', '?')
        loint = cons.get('dt', {}).get('lourb', {}).get('loint', {})
        pt = loint.get('pt', '?')
        pu = loint.get('pu', '?')
        es = loint.get('es', '?')

        if pt == '00':
            planta = 'Bajo'
        elif pt.startswith('0'):
            planta = f'Planta {pt.lstrip("0")}'
        elif pt.lstrip('-').isdigit():
            planta = f'Planta {pt}'
        else:
            planta = f'Planta {pt}'

        constructions.append({
            'planta': planta,
            'tipo': tipo,
            'superficie': stl,
            'puerta': pu,
            'escalera': es,
        })

    # Construcciones de la web
    web_constructions = []
    if datos_web and datos_web.get('construcciones'):
        for cons in datos_web['construcciones']:
            web_constructions.append({
                'uso': cons.get('uso', '?'),
                'planta': cons.get('planta', '?'),
                'superficie': cons.get('superficie', '?'),
            })

    # ── Construir documento ────────────────────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2*cm,
        title=f"Informe Catastral — {ref_completa}",
        author="Gerion Agent",
        subject=f"Datos catastrales del inmueble {ldt}",
    )

    styles = get_styles()
    story = []

    # ── Bloque: Referencia y Dirección ────────────────────────────
    ref_block = [
        [
            Paragraph('<b>Ref. Catastral</b>', styles['label']),
            Paragraph('<b>Dirección</b>', styles['label']),
        ],
        [
            Paragraph(ref_completa, styles['value_large']),
            Paragraph(ldt, styles['value']),
        ],
    ]
    ref_table = Table(ref_block, colWidths=[6*cm, 11*cm])
    ref_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_HEADER_BG),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor("#eef3f8")),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(KeepTogether([ref_table]))
    story.append(Spacer(1, 6))

    # ── Sección: Datos del Inmueble ──────────────────────────────
    story.append(_section_header("Datos del Inmueble", styles))
    story.append(Spacer(1, 2))

    datos_block = []
    row1 = [
        Paragraph('<b>Uso</b>', styles['label']),
        Paragraph('<b>Superficie construida</b>', styles['label']),
        Paragraph('<b>Año de construcción</b>', styles['label']),
        Paragraph('<b>Superficie parcela</b>', styles['label']),
    ]
    row2 = [
        Paragraph(uso, styles['value']),
        Paragraph(f"{sfc} m²", styles['value']),
        Paragraph(str(ant), styles['value']),
        Paragraph(f"{sup_parcela} m²" if sup_parcela else "—", styles['value']),
    ]
    datos_block.append(row1)
    datos_block.append(row2)

    datos_table = Table(datos_block, colWidths=[4.25*cm]*4)
    datos_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e8e8e8")),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (-1, 1), white),
    ]))
    story.append(datos_table)
    story.append(Spacer(1, 10))

    # ── Sección: Distribución por Plantas ────────────────────────
    if constructions:
        story.append(_section_header("Distribución por Plantas", styles))
        story.append(Spacer(1, 2))

        dist_header = [
            Paragraph('<b>Planta</b>', styles['label']),
            Paragraph('<b>Tipo</b>', styles['label']),
            Paragraph('<b>Superficie</b>', styles['label']),
            Paragraph('<b>Puerta</b>', styles['label']),
        ]
        dist_data = [dist_header]
        for i, cons in enumerate(constructions):
            bg = COLOR_ALT_ROW if i % 2 == 0 else white
            dist_data.append([
                Paragraph(cons['planta'], styles['value']),
                Paragraph(cons['tipo'], styles['value']),
                Paragraph(f"{cons['superficie']} m²", styles['value']),
                Paragraph(cons['puerta'], styles['value']),
            ])

        dist_table = Table(dist_data, colWidths=[4.25*cm, 5*cm, 3.75*cm, 3*cm])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e8e8e8")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            *[('BACKGROUND', (0, i+1), (-1, i+1), COLOR_ALT_ROW if i % 2 == 0 else white)
              for i in range(len(constructions))],
        ]))
        story.append(dist_table)
        story.append(Spacer(1, 10))

    # ── Sección: Construcciones (web) ────────────────────────────
    if web_constructions:
        story.append(_section_header("Construcciones (datos detallados)", styles))
        story.append(Spacer(1, 2))

        web_header = [
            Paragraph('<b>Uso</b>', styles['label']),
            Paragraph('<b>Planta</b>', styles['label']),
            Paragraph('<b>Superficie</b>', styles['label']),
        ]
        web_data = [web_header]
        for i, cons in enumerate(web_constructions):
            bg = COLOR_ALT_ROW if i % 2 == 0 else white
            web_data.append([
                Paragraph(cons['uso'], styles['value']),
                Paragraph(cons['planta'], styles['value']),
                Paragraph(f"{cons['superficie']} m²", styles['value']),
            ])

        web_table = Table(web_data, colWidths=[7*cm, 4*cm, 6*cm])
        web_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e8e8e8")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            *[('BACKGROUND', (0, i+1), (-1, i+1), COLOR_ALT_ROW if i % 2 == 0 else white)
              for i in range(len(web_constructions))],
        ]))
        story.append(web_table)
        story.append(Spacer(1, 10))

    # ── Sección: Plano de la Parcela ──────────────────────────────
    if plano_path and os.path.exists(plano_path):
        story.append(_section_header("Plano de la Parcela", styles))
        story.append(Spacer(1, 4))
        try:
            img = RLImage(plano_path, width=8*cm, height=8*cm)
            story.append(img)
        except Exception as e:
            story.append(Paragraph(f"(No se pudo insertar la imagen del plano: {e})", styles['small']))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"Ref. parcela: {ref_parcela}", styles['small']))

    # ── Sección: Mapa Satélite ───────────────────────────────────
    if satelite_path and os.path.exists(satelite_path):
        story.append(Spacer(1, 8))
        story.append(_section_header("Vista Satélite", styles))
        story.append(Spacer(1, 4))
        try:
            img = RLImage(satelite_path, width=14*cm, height=9.3*cm)
            story.append(img)
        except Exception as e:
            story.append(Paragraph(f"(No se pudo insertar la imagen de satélite: {e})", styles['small']))

    # ── Nota al pie ──────────────────────────────────────────────
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER))
    story.append(Spacer(1, 4))
    nota = (
        "Este informe se genera de forma automática a partir de datos públicos del Catastro Español. "
        "No constituye documento oficial ni certificado. Para datos con valor legal, utilice la "
        "Sede Electrónica del Catastro con certificado digital."
    )
    story.append(Paragraph(nota, styles['footer']))

    # ── Construir con cabecera personalizada ─────────────────────
    doc.build(
        story,
        onFirstPage=_draw_header,
        onLaterPages=_draw_header,
    )

    return output_path


# ─── Funciones auxiliares ──────────────────────────────────────────
def _section_header(title: str, styles) -> Table:
    """Devuelve una fila coloreada con el título de sección."""
    cell = Paragraph(title.upper(), styles['section_header'])
    t = Table([[cell]], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_SUBHEADER_BG),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def _draw_header(c, doc):
    """Dibuja la cabecera en cada página del PDF."""
    w, h = A4

    # Barra superior
    c.setFillColor(COLOR_HEADER_BG)
    c.rect(0, h - 1.6*cm, w, 1.6*cm, fill=1, stroke=0)

    # Título
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(1.5*cm, h - 1.05*cm, "INFORME CATASTRAL")
    c.setFont('Helvetica', 8)
    c.drawRightString(w - 1.5*cm, h - 0.8*cm, "Sede Electrónica del Catastro")
    c.setFont('Helvetica', 7)
    c.drawString(1.5*cm, h - 1.35*cm, "Datos no oficiales — solo con carácter informativo")

    # Línea decorativa naranja
    c.setFillColor(COLOR_SUBHEADER_BG)
    c.rect(0, h - 1.65*cm, w, 0.08*cm, fill=1, stroke=0)

    # Pie de página
    c.setFillColor(COLOR_MUTED)
    c.setFont('Helvetica', 7)
    c.drawCentredString(
        w / 2, 0.6*cm,
        f"Página {c.getPageNumber()}  |  Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Ref. {doc.title}"
    )


# ─── CLI ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Genera un informe PDF de datos catastrales.')
    parser.add_argument('provincia', help='Provincia (ej: Sevilla, Córdoba)')
    parser.add_argument('municipio', help='Municipio (ej: Utrera, Montilla)')
    parser.add_argument('calle', help='Nombre de la calle')
    parser.add_argument('numero', nargs='?', help='Número')
    parser.add_argument('--plano', '-p', help='Ruta a imagen del plano')
    parser.add_argument('--satelite', '-s', help='Ruta a imagen de satélite')
    parser.add_argument('--output', '-o', default='/tmp/informe_catastral.pdf', help='Ruta del PDF')

    args = parser.parse_args()

    # Importar el módulo catastro_full para reutilizar sus funciones
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import catastro_full

    print(f"Consultando: {args.calle} {args.numero or ''}, {args.municipio} ({args.provincia})...")

    # Consulta API
    datos_api = catastro_full.consultar_api(
        args.provincia, args.municipio, args.calle, args.numero
    )
    if not datos_api:
        print("Error en la consulta API")
        return 1

    # Scraping web
    rc_data = catastro_full.extraer_ref_catastral(datos_api)
    datos_web = None
    if rc_data:
        print("Extrayendo datos de sedecatastro.gob.es...")
        datos_web = catastro_full.scraping_sedecatastro(rc_data)

    # Generar PDF
    print(f"Generando PDF: {args.output}")
    output = generar_informe_catastral(
        datos_api=datos_api,
        datos_web=datos_web,
        output_path=args.output,
        plano_path=args.plano,
        satelite_path=args.satelite,
    )
    print(f"PDF generado: {output}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
