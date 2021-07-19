import aiohttp
from . local_settings import WORDS_API_URL_RANDOM, WORDS_API_URL_ALL

async def get_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_RANDOM) as response:
            return await response.json()

async def get_next(pk):
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_ALL + '/' +str(pk)) as response:
            status = response.status
            if status == 200:
                return await response.json()
            return None