import aiohttp
#========================================================================

class Shortners:

    def __init__(self, api, site):
        self.apis = api
        self.site = site
        self.seon = aiohttp.ClientSession

    async def shortlink(self, recived):
        try:
            async with self.seon() as seion:
                param = {'api': self.apis, 'url': recived}
                async with seion.get(self.site, params=param) as res:
                    if res.status == "success" or res.status == 200:
                        dataes = await res.json()
                        return dataes["shortenedUrl"]
                    else:
                        return None
        except Exception as e:
            print(e)
            return None

#========================================================================
