"""Utility that returns ccxt async instances, already authenticated"""
import ccxt.async_support as ccxt_async
from .config import settings

async def make_exchange(name: str):
    name = name.lower()
    klass = getattr(ccxt_async, name)
    creds = settings.API_KEYS.get(name, {})
    exch = klass({
        "apiKey": creds.get("key"),
        "secret": creds.get("secret"),
        "password": creds.get("passphrase"),
        "enableRateLimit": True,
        "timeout": 10000,
    })
    await exch.load_markets()
    return exch
