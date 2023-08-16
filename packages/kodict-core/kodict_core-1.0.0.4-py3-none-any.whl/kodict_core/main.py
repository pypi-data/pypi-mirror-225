import aiohttp
import asyncio

from .services.deepl import fetch_deepl
from .services.krdict import fetch_krdict

async def fetch_all(text: str, krdict_key: str=None, deepl_key: str=None):
    # Try Krdict API and Parser first
    results = await fetch_krdict(text, krdict_key)
    if results:
        return {"krdict": results}
    # Try DeepL
    deepl_text = await fetch_deepl(text, deepl_key)
    if deepl_text:
        results = await fetch_krdict(deepl_text, krdict_key)
    if results:
        return {"krdict": results, "deepl": deepl_text}
    else:
        return {"deepl": deepl_text}
