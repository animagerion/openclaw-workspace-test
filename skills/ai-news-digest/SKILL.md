---
name: ai-news-digest
description: Recopila noticias AI del día, redacta un artículo original y lo sube a Google Drive.
---

# AI News Digest

Recopila automáticamente noticias, papers y artículos sobre IA del día, redacta un digest original de ~1000 palabras y lo sube a Drive.

## Fuentes RSS

- **Hacker News (AI):** https://hnrss.org/newest?q=AI
- **arXiv cs.AI:** https://rss.arxiv.org/rss/cs.AI
- **TechCrunch AI:** https://techcrunch.com/category/artificial-intelligence/feed/
- **VentureBeat AI:** https://venturebeat.com/ai/feed/
- **importances AI:** https://importances.com/r/4R7pDx7o
- **机器之心 (jiqizhixin):** https://aikai.app/feed
- **量子位 (qubit):** https://qubit.cn/feed

## Estructura del digest

El artículo (~1000 palabras) sigue esta estructura:

1. **Ecosistema AI** — movimientos, announcements, modelos nuevos
2. **Empresas y Valoraciones** — financiación, M&A, resultados, analysis
3. **Aplicaciones Empresariales** — casos de uso reales, enterprise
4. **Maker / Open Source** — proyectos, herramientas, código abierto
5. **Finanzas** — stocks AI, VC funding, mercado

## Uso bajo demanda

```bash
/home/gerion/.openclaw/workspace/skills/ai-news-digest/run.sh
```

## Flujo completo

1. `collect.py` — descarga y parsea los RSS, extrae títulos/resúmenes/URLs
2. `articles.md` — raw recopilado
3. Gerion redacta el digest en Markdown
4. Subagente editor revisa y mejora
5. `upload.sh` — sube a Google Drive → carpeta `AI Weekly Digest`
6. Enlace enviado por Telegram a Paduel

## Config

- **Drive folder ID:** `13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk`
- **Drive folder link:** https://drive.google.com/drive/folders/13QjL_Sy4_fYG8GY5b8Q5kfOs16z8cIKk
- **Account:** animagerion@gmail.com
