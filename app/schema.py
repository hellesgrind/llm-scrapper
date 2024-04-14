from pydantic import BaseModel
from typing import List, Dict


class ScrapperPayload(BaseModel):
    url: str
    scrapper_schemas: List[Dict]


class PageNode(BaseModel):
    temp_id: int
    node_type: str
    source: str
    properties: Dict


class PageEdge(BaseModel):
    type: str = "CONNECTED"
    from_temp_id: int
    to_temp_id: int
    source: str


class PageGraph(BaseModel):
    nodes: List[PageNode]
    edges: List[PageEdge]


class NodeInfo(BaseModel):
    uuid: str
    type: str
    source: str
    properties: Dict


class EdgeInfo(BaseModel):
    from_uuid: str
    to_uuid: str
    type: str
    source: str
