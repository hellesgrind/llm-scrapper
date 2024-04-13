from pydantic import BaseModel
from typing import Dict


class ScrapperPayload(BaseModel):
    url: str
    scrapper_schema: Dict
