from typing import List

import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str):
        self.url = url
        self.title: str | None = None
        self.body_text: str | None = None
        self.links: List[str] | None = None

    def parse(self):
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
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
        self.title = title
        self.body_text = body_text
        self.links = annotated_links
