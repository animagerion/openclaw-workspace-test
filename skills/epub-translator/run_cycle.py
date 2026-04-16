#!/usr/bin/env python3
"""
run_cycle.py — Ciclo de traducción de un capítulo.
Spawnea un subagente que traduce el siguiente capítulo pendiente.

Uso:
  python3 run_cycle.py --init <config.json>     — Inicializa (solo primera vez)
  python3 run_cycle.py --next                    — Traduce siguiente capítulo
  python3 run_cycle.py --status                 — Muestra progreso
  python3 run_cycle.py --build                  — Genera EPUB final
"""

import sys
import os
import json
import subprocess
import glob
from pathlib import Path

WORKSPACE = "/home/gerion/.openclaw/workspace"
SKILL_DIR = f"{WORKSPACE}/skills/epub-translator"
PROGRESS_FILE = f"{SKILL_DIR}/progress.json"
CONFIG_FILE = f"{SKILL_DIR}/config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return None

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def get_next_chapter(chapters_dir):
    """Encuentra el siguiente capítulo sin traducir."""
    index_path = f"{chapters_dir}/chapters_index.json"
    if not os.path.exists(index_path):
        return None
    
    with open(index_path, 'r') as f:
        chapters = json.load(f)
    
    for ch in chapters:
        trans_file = f"{chapters_dir}/translated_{ch['file']}"
        if not os.path.exists(trans_file):
            return ch
    
    return None  # Todos traducidos

def get_prompt_path():
    return f"{SKILL_DIR}/translate_chapter.md"

def run_subagent(chapter, chapters_dir, config):
    """Spawnnea un subagente para traducir un capítulo."""
    
    chapter_num = chapter['num']
    original_file = chapter['path']
    
    # Leer contenido original
    with open(original_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Separar metadatos y texto
    parts = content.split('---\n', 2)
    meta = parts[0] if len(parts) > 0 else ""
    text = parts[1] if len(parts) > 1 else content
    
    task = f"""Traduce el siguiente capítulo del libro "{config['book_title']}" de Emad Mostaque al español.

Título del capítulo: {chapter['title']}

--- CONTENIDO DEL CAPÍTULO ---
{text}
--- FIN DEL CONTENIDO ---

Instrucciones:
- Traduce al español de España
- Mantén el tono profesional y técnico del original
- Conserva los nombres propios, terminología técnica y referencias
- No traduzcas expresiones entrecomilladas que sean术语 del autor
- El resultado final debe ser texto plano, sin marcadores ni notas
- Pega SOLO la traducción, sin comentarios tuyos
"""
    
    return task

def init(config):
    """Descarga EPUB de Drive, extrae capítulos, inicializa progreso."""
    
    chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
    os.makedirs(chapters_dir, exist_ok=True)
    
    print(f"Descargando EPUB de Drive...")
    
    # Descargar con gog
    file_id = config['drive_file_id']
    
    # Guardar EPUB original
    epub_path = f"{chapters_dir}/original.epub"
    
    cmd = f"""export PATH="/home/gerion/.local/bin:$PATH" && export GOG_KEYRING_PASSWORD="gerion-gog-2026" && export GOG_ACCOUNT="animagerion@gmail.com" && /home/gerion/.local/bin/gog drive download "{file_id}" --output "{epub_path}" 2>&1"""
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error descargando: {result.stderr}")
        # Intentar con gog drive cat si download falla
        print("Intentando método alternativo...")
        return False
    
    print(f"EPUB descargado: {epub_path}")
    
    # Extraer capítulos
    import subprocess
    parse_cmd = f"python3 {SKILL_DIR}/parse_epub.py {epub_path} {chapters_dir}"
    result = subprocess.run(parse_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error extrayendo capítulos: {result.stderr}")
        return False
    
    print(result.stdout)
    
    # Inicializar progreso
    index_path = f"{chapters_dir}/chapters_index.json"
    with open(index_path, 'r') as f:
        chapters = json.load(f)
    
    progress = {
        'book_title': config['book_title'],
        'book_title_es': config.get('book_title_es', config['book_title']),
        'author': config.get('author', 'Unknown'),
        'total_chapters': len(chapters),
        'chapters': [{'num': ch['num'], 'title': ch['title'], 'done': False, 'source': ch['source']} for ch in chapters],
        'current': 0
    }
    
    save_progress(progress)
    print(f"\nProgreso inicializado. {len(chapters)} capítulos detectados.")
    print("Ejecuta run_cycle.py --next para traducir el capítulo 1.")
    
    return True

def next_chapter():
    """Traduce el siguiente capítulo pendiente."""
    
    config = load_config()
    chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
    
    # Encontrar siguiente capítulo
    chapter = get_next_chapter(chapters_dir)
    
    if chapter is None:
        print("Todos los capítulos han sido traducidos.")
        print("Ejecuta run_cycle.py --build para generar el EPUB final.")
        return False
    
    chapter_num = chapter['num']
    print(f"Procesando capítulo {chapter_num}: {chapter['title']}")
    
    # Generar task
    task = run_subagent(chapter, chapters_dir, config)
    
    # Escribir task a archivo temporal para el subagente
    task_file = f"{SKILL_DIR}/current_task.md"
    with open(task_file, 'w') as f:
        f.write(task)
    
    print(f"Task escrita en {task_file}")
    print(f"Capítulo: {chapter_num}/{config.get('total_chapters', '?')}")
    
    return True

def status():
    """Muestra el estado actual de la traducción."""
    
    progress = load_progress()
    if not progress:
        print("No hay progreso. Ejecuta run_cycle.py --init primero.")
        return
    
    total = progress['total_chapters']
    done = sum(1 for ch in progress['chapters'] if ch.get('done', False))
    
    print(f"\n=== PROGRESO DE TRADUCCIÓN ===")
    print(f"Libro: {progress['book_title_es']} ({progress['book_title']})")
    print(f"Progreso: {done}/{total} capítulos ({100*done//total}%)")
    print()
    
    for ch in progress['chapters']:
        status_icon = "✅" if ch.get('done') else "⏳"
        print(f"  {status_icon} Cap.{ch['num']:03d}: {ch['title']}")

def build():
    """Genera el EPUB final con todas las traducciones."""
    
    config = load_config()
    chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
    epub_path = f"{chapters_dir}/original.epub"
    output_path = f"{chapters_dir}/../{config['book_title_es'].replace(' ', '_')}_es.epub"
    
    cmd = f"python3 {SKILL_DIR}/build_epub.py {epub_path} {chapters_dir} {output_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error generando EPUB: {result.stderr}")
        return False
    
    print(result.stdout)
    print(f"\nEPUB final: {output_path}")
    
    # Subir a Drive
    output_folder = config.get('output_folder', 'Libros/Traducidos')
    print(f"\nSubiendo a Drive en carpeta: {output_folder}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == '--init':
        if len(sys.argv) < 3:
            print("Uso: run_cycle.py --init <config.json>")
            sys.exit(1)
        config_path = sys.argv[2]
        with open(config_path, 'r') as f:
            config = json.load(f)
        init(config)
    
    elif cmd == '--next':
        next_chapter()
    
    elif cmd == '--status':
        status()
    
    elif cmd == '--build':
        build()
    
    else:
        print(f"Comando desconocido: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()