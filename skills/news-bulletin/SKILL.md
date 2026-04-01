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

## Uso bajo demanda

```bash
python3 /home/gerion/.openclaw/workspace/skills/news-bulletin/collect.py
```

## Flujo

1. `collect.py` — descarga y parsea los RSS (múltiples fuentes), extrae títulos, resúmenes y URLs
2. `raw_news.md` — raw recopilado y organizado por categoría
3. Gerion redacta el boletín en Markdown (texto completo)
4. Genera audio TTS con voice "AlvaroNeutral" (Edge TTS)
5. Envía el audio por Telegram a Paduel
6. También envía el texto del boletín como mensaje o documento

## Configuración

- **Idioma:** Español de España
- **Voice:** AlvaroNeutral (Edge TTS)
- **Salida audio:** `/tmp/news_bulletin.mp3`
- **Salida texto:** `/tmp/news_bulletin.md`

## Notas

- Priorizar noticias del día (no de días anteriores)
- Incluir 3-5 noticias por sección
- Mantener tono profesional de informativo
- Filtrar noticias antiguas o duplicadas
- Si una fuente falla, continuar con las demás
