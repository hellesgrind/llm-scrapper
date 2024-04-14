from typing import Dict
import uuid

from database import DatabaseIntegration
from schema import (
    PageGraph,
    PageNode,
    PageEdge,
    NodeInfo,
    EdgeInfo,
)
from logs import logger


class DataManager:
    def __init__(
        self,
        db_integration: DatabaseIntegration,
    ):
        self.db_integration = db_integration
        self.temp_id_to_id: Dict | None = None

    async def insert_data(self, data: PageGraph):
        self.temp_id_to_id = {}
        nodes = data.nodes
        edges = data.edges
        for node in nodes:
            await self.insert_node(node)
        for edge in edges:
            await self.insert_edge(edge)

    async def insert_node(self, node: PageNode):
        node_uuid = str(uuid.uuid4())
        self.temp_id_to_id[node.temp_id] = node_uuid
        node_info = NodeInfo(
            type=node.node_type,
            uuid=node_uuid,
            source=node.source,
            properties=node.properties,
        )
        await self.db_integration.add_node(node_info)

    async def insert_edge(self, edge: PageEdge):
        from_uuid = self.temp_id_to_id.get(edge.from_temp_id)
        to_uuid = self.temp_id_to_id.get(edge.to_temp_id)

        if not from_uuid or not to_uuid:
            logger.error("UUID not found for one or more temp_ids")
            return
        edge_info = EdgeInfo(
            from_uuid=from_uuid,
            to_uuid=to_uuid,
            source=edge.source,
            type=edge.type,
        )
        await self.db_integration.add_edge(edge_info)
