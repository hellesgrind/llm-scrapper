import requests
from typing import Type
from pydantic import BaseModel
from utils import generate_json_schema

APP_ENDPOINT = "http://0.0.0.0:8000"


class Employee(BaseModel):
    name: str
    position: str


def scrape_url(
    url: str,
    scrapper_schema: Type[BaseModel],
):
    payload = {
        "url": url,
        "scrapper_schema": generate_json_schema(scrapper_schema),
    }
    requests.post(
        url=f"{APP_ENDPOINT}/scrapper",
        json=payload,
    )


if __name__ == "__main__":
    scrape_url(
        url="https://www.apple.com/leadership/",
        scrapper_schema=Employee,
    )
