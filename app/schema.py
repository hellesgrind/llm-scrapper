from pydantic import BaseModel
from typing import List, Dict


class ScrapperPayload(BaseModel):
    url: str
    scrapper_schemas: List[Dict]


class Node(BaseModel):
    temp_id: int
    node_type: str
    source: str
    properties: Dict


class Edge(BaseModel):
    from_temp_id: int
    to_temp_id: int
    source: str


class PageGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
