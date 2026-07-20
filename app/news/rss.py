import time

import feedparser

CACHE_TTL_SECONDS = 600  # 10 minutes

RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
}

_cache = {
    "articles": None,
    "timestamp": 0,
}


def get_latest_articles(limit=20):
    """Retourne les derniers articles crypto (RSS), avec cache de 10 min."""
    now = time.time()

    if _cache["articles"] is not None and (now - _cache["timestamp"]) < CACHE_TTL_SECONDS:
        return _cache["articles"][:limit]

    articles = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue

        for entry in feed.entries[:15]:
            published_parsed = entry.get("published_parsed")
            published_ts = time.mktime(published_parsed) if published_parsed else 0

            articles.append({
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", "#"),
                "source": source,
                "published": entry.get("published", ""),
                "published_ts": published_ts,
            })

    if not articles:
        # API/flux indisponible : on retombe sur le cache existant si possible
        return _cache["articles"][:limit] if _cache["articles"] is not None else []

    articles.sort(key=lambda a: a["published_ts"], reverse=True)

    _cache["articles"] = articles
    _cache["timestamp"] = now
    return articles[:limit]
