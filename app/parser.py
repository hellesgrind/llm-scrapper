from typing import List

import aiohttp
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str, title: str, body_text: str, links: List[str]):
        self.url = url
        self.title = title
        self.body_text = body_text
        self.links = links

    @classmethod
    async def parse(cls, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        annotated_links = []

        if soup.title:
            title = soup.title.string
        else:
            title = "No title found"
        if soup.body:
            body_text = soup.body.get_text(separator=" ", strip=True)
        else:
            body_text = "No text found"
        for element in soup.find_all(["p", "a"]):
            if element.name == "a" and element.get("href"):
                link_text = (
                    f"{element.get_text(separator=' ', strip=True)} "
                    f"[Sublink: {element['href']}]"
                )
                annotated_links.append(link_text)
            else:
                annotated_links.append(element.text)
        self = cls(
            url=url,
            title=title,
            body_text=body_text,
            links=annotated_links,
        )
        return self
