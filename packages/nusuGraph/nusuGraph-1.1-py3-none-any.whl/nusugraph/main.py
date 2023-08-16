import httpx
import asyncio
import json
from .utils import html_to_nodes


class Telegraph:
    def __init__(self, token: str = None, timeout: int = 10, tokenList: list or tuple = None):
        self.__ses = httpx.AsyncClient(timeout=timeout)
        self.__token = token
        self.__tokenList = tokenList
        self.__length = len(tokenList) if tokenList else 0
        self.__count = 0

    async def getToken(self):
        if self.__token:
            return self.__token

        if not self.__token and not self.__tokenList:
            res = await self.createAccount()
            self.__token = res.get("access_token")
            return self.__token

        if self.__count >= self.__length:
            self.__count = 0

        x = self._tokens[self.__count]
        self.__count += 1
        return x

    async def createAccount(self, shortName: str = "Anonymous", authorName: str = "Anonymous", authorUrl: str = None):
        url = "https://api.telegra.ph/createAccount"
        params = {
            "short_name": shortName,
            "author_name": authorName,
            "author_url": authorUrl
        }
        res = (await self.__ses.get(url, params=params)).json()

        return res["result"] if res["ok"] else res

    async def createPage(self, author: str, htmlContent: str, title: str, returnContent: bool = False):
        if not self.__token:
            print("Access Token Not Found. An Anonymous Account Will Be Created")

        url = "https://api.telegra.ph/createPage"
        token = await self.getToken()
        # "d3b25feccb89e508a9114afb82aa421fe2a9712b963b387cc5ad71e58722"

        params = {
            "access_token": token,
            "title": title,
            "author_name": author,
            "content": json.dumps(html_to_nodes(htmlContent)),
            "return_content": returnContent
        }
        res = (await self.__ses.get(url, params=params)).json()
        return res["result"] if res["ok"] else res


async def main():
    graph = Telegraph(timeout=None)
    text = "<b>Hello from the other side</b>"
    author = "Nusab Taha"
    title = "Testing"
    res = await graph.createPage(author, text, title)
    print(res)
    a = [graph.createPage(author, text, title) for i in range(10)]
    a = await asyncio.gather(*a)
    print(*a, sep="\n")

if __name__ == "__main__":
    asyncio.run(main())
