import aiohttp
from Shortner.script import Scripted
#====================================================================

async def Slink(SHORTNER, API, URL):
    midos = {'api': API, 'url': URL}
    async with aiohttp.ClientSession() as session:
        async with session.get(SHORTNER, params=midos) as res:
            if res.status == "success" or res.status == 200:
                dataes = await res.json()
                ourais = dataes["shortenedUrl"]
                return ourais
            else:
                return URL

#====================================================================
