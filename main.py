import requests
from typing import Type, List
from pydantic import BaseModel
from utils import prepare_schema

APP_ENDPOINT = "http://0.0.0.0:8000"


class Position(BaseModel):
    position_name: str
    company_name: str


class Education(BaseModel):
    school_name: str


class Employee(BaseModel):
    name: str


def scrape_url(
    url: str,
    scrapper_schemas: List[Type[BaseModel]],
):
    schemas = []
    for schema in scrapper_schemas:
        schemas.append(prepare_schema(schema))
    payload = {
        "url": url,
        "scrapper_schemas": schemas,
    }
    requests.post(
        url=f"{APP_ENDPOINT}/scrapper",
        json=payload,
    )


if __name__ == "__main__":
    scrape_url(
        url="https://www.apple.com/leadership/craig-federighi/",
        scrapper_schemas=[Employee, Position, Education],
    )
