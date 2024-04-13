from pydantic import BaseModel
from typing import Dict
from pydantic import (
    AnyUrl,
)


class ScrapperPayload(BaseModel):
    url: AnyUrl
    model: Dict
