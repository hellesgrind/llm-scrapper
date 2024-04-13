from pydantic import BaseModel
from typing import List, Dict


class ScrapperPayload(BaseModel):
    url: str
    scrapper_schemas: List[Dict]
