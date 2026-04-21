---
name: news-bulletin
description: Recopila noticias internacionales y españolas de fuentes variadas, redacta un boletín detallado en texto y lo convierte en audio TTS.
---

# News Bulletin — Boletín de Noticias Internacional

Recopila noticias del día de fuentes internacionales y españolas con distintos sesgos, redacta un boletín detallado en texto, y lo convierte en audio TTS.

## Fuentes RSS

### Internacionales (varios sesgos)
- **Reuters:** https://feeds.reuters.com/reuters/topNews
- **AP:** https://apnews.com/rss
- **BBC World:** https://feeds.bbci.co.uk/news/world/rss.xml
- **The Guardian World:** https://www.theguardian.com/world/rss
- **El País Internacional:** https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada
- **Le Monde:** https://www.lemonde.fr/international/rss_full.xml
- **Der Spiegel:** https://www.spiegel.de/international/index.rss
- **The Economist:** https://www.economist.com/international/rss.xml

### España
- **El País España:** https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada
- **El Mundo:** https://www.elmundo.es/elmundo/hemeroteca/rss/portada.xml
- **ABC:** https://www.abc.es/rss/feeds/abcPortada.xml
- **La Vanguardia:** https://www.lavanguardia.com/rss/home.xml
- **El Confidencial:** https://www.elconfidencial.com/feeds/latest/
- **Público:** https://www.publico.es/rss/
- **elDiario.es:** https://www.eldiario.es/rss/

### Economía
- **Financial Times:** https://www.ft.com/?format=rss
- **Bloomberg:** https://feeds.bloomberg.com/markets/news.rss
- **Expansión:** https://e00-elmundo.uecdn.es/expansion/rss/expansion Portada.xml

## Estructura del boletín

El boletín sigue esta estructura (~1500-2000 palabras):

1. **INTERNACIONAL** — noticias destacadas del día en el mundo
2. **EUROPA** — noticias europeas relevantes
3. **ESPAÑA** — política, sociedad, economía española
4. **ECONOMÍA** — mercados, empresas, finanzas internacionales
5. **BREVES** — otras noticias de interés

## Fuentes RSS

Las fuentes RSS son el método principal de recopilación. Ver `collect.py` para la lista completa.

### Mejora con Obscura

Para artículos individuales que necesitan más detalle (contenido completo, JS rendering):

```bash
obscura fetch <url> --wait-until networkidle0 --dump text --quiet
```

Usar Obscura cuando:
- Una fuente no tiene RSS funcional
- El RSS solo da resumen y necesitamos el artículo completo
- La web carga contenido dinámicamente (JavaScript)
- RSS falla o está bloqueado

### Ejemplo de uso con Obscura para una noticia

```bash
# Scraping completo de un artículo
URL="https://www.elconfidencial.com/..."
obscura fetch "$URL" --stealth --wait-until networkidle0 --dump text > /tmp/article.txt
```

## Uso bajo demanda

```bash
python3 /home/gerion/.openclaw/workspace/skills/news-bulletin/collect.py
```

Para forzar re-scraping con Obscura en lugar de caché:
```bash
python3 /home/gerion/.openclaw/workspace/skills/news-bulletin/collect.py --no-cache
```

## Flujo

1. `collect.py` — descarga y parsea los RSS (múltiples fuentes), extrae títulos, resúmenes y URLs
2. `raw_news.md` — raw recopilado y organizado por categoría
3. Gerion redacta el borrador del boletín en Markdown
4. **REVISIÓN Y EDICIÓN FINAL** — Antes de generar el audio, revisar el borrador aplicando estos criterios:
   - ¿Hay texto en otros idiomas (chino, etc.) que se haya colado por error?
   - ¿Hay abreviaturas o términos en inglés sin explicar?
   - ¿La estructura es clara y coherente?
   - ¿El tono es profesional y está en español correcto?
   - ¿Hay datos incorrectos o inventados?
   - ¿Falta contexto que el lector pueda necesitar?
   - ¿El cierre es adecuado (recordatorio de agenda si aplica)?
   Corregir todo lo que falle antes de pasar al audio.
5. Genera audio TTS con voice "AlvaroNeutral" (Edge TTS)
6. Envía el audio por Telegram a Paduel
7. También envía el texto del boletín como mensaje o documento

## Configuración

- **Idioma:** Español de España
- **Voice:** AlvaroNeutral (Edge TTS)
- **Salida audio:** `/tmp/news_bulletin.mp3`
- **Salida texto:** `/tmp/news_bulletin.md`

## Notas

- Si una fuente RSS falla o está bloqueada, usar Obscura como fallback:
  ```bash
  obscura fetch <url> --dump html --quiet
  ```
- Priorizar noticias del día (no de días anteriores)
- Incluir 3-5 noticias por sección
- Mantener tono profesional de informativo
- Filtrar noticias antiguas o duplicadas
- Si una fuente falla, continuar con las demás