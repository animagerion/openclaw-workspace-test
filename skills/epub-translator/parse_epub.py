#!/usr/bin/env python3
"""
parse_epub.py — Extrae capítulos de un EPUB a texto plano.
Uso: python3 parse_epub.py <archivo.epub> <carpeta_salida>
"""

import sys
import os
import json
import zipfile
import re
from pathlib import Path
import ebooklib
from ebooklib import epub

def extract_epub(epub_path, output_dir):
    """Extrae los capítulos de un EPUB y los guarda como archivos de texto."""
    
    book = epub.read_epub(epub_path)
    
    chapters = []
    chapter_num = 0
    
    for item in book.get_items():
        if item.get_type() == 9:  # EPUB = 9
            content = item.get_content().decode('utf-8', errors='replace')
            
            # Extraer texto del HTML
            text = html_to_text(content)
            
            if len(text.strip()) < 200:
                continue
            
            chapter_num += 1
            chapter_file = f"chapter_{chapter_num:03d}.txt"
            chapter_path = os.path.join(output_dir, chapter_file)
            
            with open(chapter_path, 'w', encoding='utf-8') as f:
                # Guardar también metadatos del capítulo
                title = extract_title(content)
                f.write(f"CHAPTER_TITLE: {title}\n")
                f.write(f"CHAPTER_NUM: {chapter_num}\n")
                f.write(f"SOURCE_FILE: {item.get_name()}\n")
                f.write("---\n")
                f.write(text)
            
            chapters.append({
                'num': chapter_num,
                'title': title,
                'file': chapter_file,
                'path': chapter_path,
                'source': item.get_name()
            })
    
    return chapters

def html_to_text(html):
    """Convierte contenido HTML a texto plano, limpiando etiquetas y normalizando."""
    
    # Eliminar scripts y estilos
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Reemplazar tags de bloque con separadores
    html = re.sub(r'<(p|div|br|h[1-6])[^>]*>', '\n', html, flags=re.IGNORECASE)
    
    # Eliminar tags restantes
    html = re.sub(r'<[^>]+>', '', html)
    
    # Normalizar espacios y líneas
    html = re.sub(r'\n\s*\n', '\n\n', html)
    html = re.sub(r'[ \t]+', ' ', html)
    html = re.sub(r'\n[ \t]+', '\n', html)
    
    # Eliminar caracteres extraños Unicode que puedan causar problemas
    # (se permiten acentos, eñe, ü, etc. de español)
    # Solo eliminar control chars y emoji muy raros
    html = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', html)
    
    return html.strip()

def extract_title(html):
    """Extrae el título del capítulo del HTML."""
    # Buscar en title, h1, h2
    match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    match = re.search(r'<h2[^>]*>([^<]+)</h2>', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return "Sin título"

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 parse_epub.py <archivo.epub> <carpeta_salida>")
        sys.exit(1)
    
    epub_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chapters = extract_epub(epub_path, output_dir)
    
    # Guardar índice
    index_path = os.path.join(output_dir, 'chapters_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)
    
    print(f"Extraídos {len(chapters)} capítulos en {output_dir}")
    for ch in chapters:
        print(f"  {ch['num']:03d}: {ch['title']}")

if __name__ == '__main__':
    main()