import requests
from typing import Type
from pydantic import BaseModel
from utils import generate_json_schema

APP_ENDPOINT = "http://0.0.0.0:8000"


class Employee(BaseModel):
    name: str
    company: str
    position: str


def scrape_url(
    url: str,
    model: Type[BaseModel],
):
    payload = {
        "url": url,
        "model": generate_json_schema(model),
    }
    requests.post(
        url=f"{APP_ENDPOINT}/scrapper",
        json=payload,
    )


if __name__ == "__main__":
    scrape_url(
        url="https://www.paulgraham.com/cities.html",
        model=Employee,
    )
