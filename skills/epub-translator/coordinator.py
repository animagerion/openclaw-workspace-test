#!/usr/bin/env python3
"""
coordinator.py — Coordina la traducción automática capítulo a capítulo.
Llamado por cron cada N minutos. Si hay capítulo pendiente, spawnea subagente.

Uso: python3 coordinator.py [--daemon <minutos_entre_ciclos>]
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path

SKILL_DIR = "/home/gerion/.openclaw/workspace/skills/epub-translator"
PROGRESS_FILE = f"{SKILL_DIR}/progress.json"
CONFIG_FILE = f"{SKILL_DIR}/config.json"
TASK_FILE = f"{SKILL_DIR}/current_task.md"

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return None
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

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
    return None

def read_chapter(chapter):
    """Lee el contenido original de un capítulo."""
    with open(chapter['path'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---\n', 2)
    meta = parts[0] if len(parts) > 0 else ""
    text = parts[1] if len(parts) > 1 else content
    
    # Extraer título del meta
    title = chapter['title']
    for line in meta.split('\n'):
        if line.startswith('CHAPTER_TITLE:'):
            title = line.replace('CHAPTER_TITLE:', '').strip()
    
    return title, text

def mark_chapter_done(progress, chapter_num):
    """Marca un capítulo como traducido."""
    for ch in progress['chapters']:
        if ch['num'] == chapter_num:
            ch['done'] = True
            break
    progress['current'] = chapter_num
    save_progress(progress)

def save_translation(chapters_dir, chapter_file, translated_text):
    """Guarda la traducción de un capítulo."""
    trans_file = f"{chapters_dir}/translated_{chapter_file}"
    with open(trans_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)
    return trans_file

def init(config):
    """Descarga EPUB de Drive y extrae capítulos. Solo primera vez."""
    
    chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
    os.makedirs(chapters_dir, exist_ok=True)
    
    file_id = config['drive_file_id']
    epub_path = f"{chapters_dir}/original.epub"
    
    # Descargar de Drive
    print("Descargando EPUB de Drive...")
    cmd = f'''export PATH="/home/gerion/.local/bin:$PATH" && export GOG_KEYRING_PASSWORD="gerion-gog-2026" && export GOG_ACCOUNT="animagerion@gmail.com" && /home/gerion/.local/bin/gog drive download "{file_id}" --output "{epub_path}"'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    
    if result.returncode != 0:
        print(f"Error descargando: {result.stderr[:500]}")
        return False
    
    print(f"EPUB descargado: {epub_path}")
    
    # Extraer capítulos
    parse_cmd = f"python3 {SKILL_DIR}/parse_epub.py {epub_path} {chapters_dir}"
    result = subprocess.run(parse_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error extrayendo: {result.stderr}")
        return False
    
    # Cargar índice
    index_path = f"{chapters_dir}/chapters_index.json"
    with open(index_path, 'r') as f:
        chapters = json.load(f)
    
    print(f"Extraídos {len(chapters)} capítulos.")
    
    # Inicializar progreso
    progress = {
        'book_title': config['book_title'],
        'book_title_es': config.get('book_title_es', config['book_title']),
        'author': config.get('author', 'Unknown'),
        'total_chapters': len(chapters),
        'chapters': [
            {'num': ch['num'], 'title': ch['title'], 'done': False, 'source': ch['source']}
            for ch in chapters
        ],
        'current': 0,
        'chapters_dir': chapters_dir,
        'epub_path': epub_path
    }
    
    save_progress(progress)
    
    # Guardar config en progreso para referencia
    progress['config'] = config
    save_progress(progress)
    
    print(f"\nInicialización completada.")
    print(f"Total: {len(chapters)} capítulos")
    
    return True

def status():
    """Muestra estado actual."""
    progress = load_progress()
    if not progress:
        print("No hay traducción en curso. Ejecuta --init primero.")
        return
    
    total = progress['total_chapters']
    done = sum(1 for ch in progress['chapters'] if ch.get('done', False))
    
    print(f"\n📖 {progress['book_title_es']}")
    print(f"   {done}/{total} capítulos traducidos ({100*done//total}%)")
    
    if done < total:
        next_ch = next((ch for ch in progress['chapters'] if not ch.get('done')), None)
        if next_ch:
            print(f"   Siguiente: Cap.{next_ch['num']:03d} — {next_ch['title']}")
    
    print()
    for ch in progress['chapters']:
        icon = "✅" if ch.get('done') else "⏳"
        print(f"   {icon} Cap.{ch['num']:03d}: {ch['title']}")

def main():
    if len(sys.argv) < 2:
        print("Uso: coordinator.py <comando> [args]")
        print("Comandos:")
        print("  --init              Inicializar (primera vez)")
        print("  --status            Ver progreso")
        print("  --next              Traducir siguiente capítulo")
        print("  --build             Generar EPUB final")
        print("  --daemon <min>      Ejecutar en bucle continuo")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == '--init':
        config = load_config()
        if not config:
            print("Crea config.json primero con drive_file_id")
            sys.exit(1)
        init(config)
    
    elif cmd == '--status':
        status()
    
    elif cmd == '--next':
        progress = load_progress()
        if not progress:
            print("Ejecuta --init primero")
            sys.exit(1)
        
        config = load_config()
        chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
        
        chapter = get_next_chapter(chapters_dir)
        if not chapter:
            print("Todos los capítulos traducidos. Ejecuta --build.")
            sys.exit(0)
        
        title, text = read_chapter(chapter)
        
        print(f"Capítulo {chapter['num']}: {title}")
        print(f"Caracteres: {len(text)}")
        
        # Guardar task
        with open(TASK_FILE, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {title}\n")
            f.write(f"CHAPTER_NUM: {chapter['num']}\n")
            f.write(f"SOURCE_FILE: {chapter['source']}\n")
            f.write("---\n")
            f.write(text)
        
        print(f"\nTask disponible en: {TASK_FILE}")
        print("Llama a sessions_spawn para traducciones.")
    
    elif cmd == '--build':
        progress = load_progress()
        if not progress:
            print("No hay progreso")
            sys.exit(1)
        
        config = load_config()
        chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
        
        output_epub = f"{SKILL_DIR}/{progress['book_title_es'].replace(' ', '_')}.epub"
        cmd = f"python3 {SKILL_DIR}/build_epub.py {progress['epub_path']} {chapters_dir} {output_epub}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print(result.stdout)
            print(f"\n✅ EPUB generado: {output_epub}")
    
    elif cmd == '--daemon':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        print(f"Daemon activo. Ciclo cada {interval} min. Ctrl+C para parar.")
        
        while True:
            progress = load_progress()
            if progress:
                config = load_config()
                chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
                
                chapter = get_next_chapter(chapters_dir)
                if chapter:
                    print(f"\n[{time.strftime('%H:%M')}] Capítulo pendiente: {chapter['num']}")
                    # Aquí se spawnea el subagente desde el agente principal
                    break
                else:
                    print(f"\n[{time.strftime('%H:%M')}] Todos traducidos. Ejecuta --build.")
                    break
            else:
                print("No hay progreso. Ejecuta --init.")
                break
            
            time.sleep(interval * 60)
    
    else:
        print(f"Comando desconocido: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()