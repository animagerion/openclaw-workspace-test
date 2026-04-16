#!/usr/bin/env python3
"""
translate_one.py — Traduce UN capítulo usando MiniMax via sessions_spawn.
Este script es llamado por el cron o manualmente para procesar un capítulo.

Uso: python3 translate_one.py <chapter_num>
"""

import sys
import os
import json
import subprocess
import base64

SKILL_DIR = "/home/gerion/.openclaw/workspace/skills/epub-translator"
PROGRESS_FILE = f"{SKILL_DIR}/progress.json"
CONFIG_FILE = f"{SKILL_DIR}/config.json"
TRANSLATE_PROMPT = f"{SKILL_DIR}/translate_chapter.md"

def load_progress():
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_chapter_info(chapters_dir, chapter_num):
    index_path = f"{chapters_dir}/chapters_index.json"
    with open(index_path, 'r') as f:
        chapters = json.load(f)
    
    for ch in chapters:
        if ch['num'] == chapter_num:
            return ch
    return None

def read_chapter(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---\n', 2)
    meta = parts[0] if len(parts) > 0 else ""
    text = parts[1] if len(parts) > 1 else content
    return meta, text

def get_translate_prompt():
    with open(TRANSLATE_PROMPT, 'r') as f:
        return f.read()

def encode_for_subagent(text):
    """Codifica el texto para pasarlo a un subagente de forma segura."""
    return base64.b64encode(text.encode('utf-8')).decode('ascii')

def main():
    if len(sys.argv) < 2:
        print("Uso: translate_one.py <chapter_num>")
        sys.exit(1)
    
    chapter_num = int(sys.argv[1])
    config = load_config()
    chapters_dir = config.get('chapters_dir', f"{SKILL_DIR}/chapters")
    
    chapter = get_chapter_info(chapters_dir, chapter_num)
    if not chapter:
        print(f"Capítulo {chapter_num} no encontrado.")
        sys.exit(1)
    
    print(f"=== Traduciendo capítulo {chapter_num}: {chapter['title']} ===")
    
    # Leer contenido original
    meta, original_text = read_chapter(chapter['path'])
    print(f"Texto original: {len(original_text)} caracteres")
    
    # Preparar prompt para subagente
    translate_system = get_translate_prompt()
    
    # El subagente recibe el capítulo y traduce
    task = f"""Eres un traductor profesional. Traduce el siguiente capítulo del libro "The Last Economy" de Emad Mostaque al español de España.

Título: {chapter['title']}

--- CONTENIDO ---
{original_text}
--- FIN ---

Sigue las instrucciones del system prompt que tienes cargado para la traducción.

Devuelve SOLO la traducción en español, sin comentarios tuyos, sin marcadores, sin nada más. Solo el texto del capítulo."""

    # Guardar task en archivo para pasarla al subagente
    task_file = f"{SKILL_DIR}/task_chapter_{chapter_num}.txt"
    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(task)
    
    print(f"\nTask guardada. Ahora spawnea el subagente de traducción.")
    print(f"Usa: sessions_spawn con runtime='subagent' y task读过 task_file")

if __name__ == '__main__':
    main()