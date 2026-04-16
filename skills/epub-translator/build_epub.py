#!/usr/bin/env python3
"""
build_epub.py — Reconstruye un EPUB con las traducciones.
Uso: python3 build_epub.py <original.epub> <carpeta_capitulos> <output.epub>
"""

import sys
import os
import json
import zipfile
import shutil
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def rebuild_epub(original_epub, chapters_dir, output_epub):
    """Reconstruye el EPUB reemplanzando capítulos originales con traducciones."""
    
    # Leer índice de capítulos
    index_path = os.path.join(chapters_dir, 'chapters_index.json')
    with open(index_path, 'r', encoding='utf-8') as f:
        chapters_meta = json.load(f)
    
    # Leer traducciones
    translations = {}
    for ch in chapters_meta:
        if ch.get('translated'):
            trans_path = os.path.join(chapters_dir, f"translated_{ch['file']}")
            if os.path.exists(trans_path):
                with open(trans_path, 'r', encoding='utf-8') as f:
                    translations[ch['source']] = f.read()
    
    # Abrir EPUB original
    book = epub.read_epub(original_epub)
    
    # Reemplazar contenido de cada capítulo
    for item in book.get_items():
        if item.get_type() == 9:  # XHTML
            source_name = item.get_name()
            
            if source_name in translations:
                original_html = item.get_content().decode('utf-8', errors='replace')
                translated_text = translations[source_name]
                
                # Reconstruir HTML con la traducción
                new_html = rebuild_chapter_html(original_html, translated_text)
                item.set_content(new_html.encode('utf-8'))
    
    # Guardar nuevo EPUB
    epub.write_epub(output_epub, book)
    print(f"EPUB reconstruido: {output_epub}")

def rebuild_chapter_html(original_html, translated_text):
    """Reconstruye el HTML del capítulo manteniendo la estructura original."""
    
    soup = BeautifulSoup(original_html, 'html.parser')
    
    # Encontrar el body y reemplazar contenido
    body = soup.find('body')
    if body:
        # Limpiar el body
        body.clear()
        
        # Dividir texto en párrafos
        paragraphs = translated_text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Crear elemento p
            p = soup.new_tag('p')
            p.string = para
            body.append(p)
            body.append('\n')
    
    return str(soup)

def main():
    if len(sys.argv) < 4:
        print("Uso: python3 build_epub.py <original.epub> <carpeta_capitulos> <output.epub>")
        sys.exit(1)
    
    original_epub = sys.argv[1]
    chapters_dir = sys.argv[2]
    output_epub = sys.argv[3]
    
    rebuild_epub(original_epub, chapters_dir, output_epub)

if __name__ == '__main__':
    main()