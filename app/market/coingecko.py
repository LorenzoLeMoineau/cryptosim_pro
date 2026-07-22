import time

import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
CACHE_TTL_SECONDS = 60

_cache = {
    "data": None,
    "timestamp": 0,
}


def get_market_data(vs_currency="usd", per_page=20):
    """Retourne la liste des cryptos triées par market cap, avec cache de 60s."""
    now = time.time()

    if _cache["data"] is not None and (now - _cache["timestamp"]) < CACHE_TTL_SECONDS:
        return _cache["data"]

    try:
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/markets",
            params={
                "vs_currency": vs_currency,
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": 1,
                "price_change_percentage": "24h",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        # API indisponible ou rate-limit atteint : on retombe sur le cache existant
        if _cache["data"] is not None:
            return _cache["data"]
        return []

    _cache["data"] = data
    _cache["timestamp"] = now
    return data


def get_coin(coin_id, vs_currency="usd"):
    """Retourne les données d'une crypto précise (id CoinGecko, ex: 'bitcoin')."""
    for coin in get_market_data(vs_currency=vs_currency):
        if coin["id"] == coin_id:
            return coin
    return None


def get_coin_price(coin_id, vs_currency="usd"):
    """Retourne uniquement le prix actuel d'une crypto, ou None si introuvable."""
    coin = get_coin(coin_id, vs_currency=vs_currency)
    return coin["current_price"] if coin else None


_chart_cache = {}
CHART_CACHE_TTL_SECONDS = 300  # 5 minutes


def get_market_chart(coin_id, vs_currency="usd", days=7):
    """Retourne l'historique de prix [[timestamp_ms, prix], ...] sur N jours, avec cache."""
    cache_key = (coin_id, vs_currency, days)
    now = time.time()
    cached = _chart_cache.get(cache_key)

    if cached is not None and (now - cached["timestamp"]) < CHART_CACHE_TTL_SECONDS:
        return cached["prices"]

    try:
        response = requests.get(
            f"{COINGECKO_API_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": vs_currency, "days": days},
            timeout=10,
        )
        response.raise_for_status()
        prices = response.json().get("prices", [])
    except requests.RequestException:
        return cached["prices"] if cached is not None else []

    _chart_cache[cache_key] = {"prices": prices, "timestamp": now}
    return prices
