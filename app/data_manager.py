from typing import Dict
import uuid

from database import DatabaseIntegration
from llm_client import OpenAIModel
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
        model: OpenAIModel,
    ):
        self.db_integration = db_integration
        self.model = model
        self.temp_id_to_id: Dict | None = None

    async def insert_data(self, data: PageGraph):
        self.temp_id_to_id = {}
        nodes = data.nodes
        edges = data.edges
        for node in nodes:
            # await self.conditional_add_node(node)
            await self.insert_node(node)
        for edge in edges:
            await self.insert_edge(edge)

    # TODO:
    async def conditional_add_node(self, node: PageNode):
        existing_nodes = await self.db_integration.get_all_nodes(
            node_type=node.node_type,
        )
        pass

    # TODO:
    async def check_if_node_exist(self, node: PageNode):
        pass

    # TODO:
    async def create_updated_node(
        self,
        existing_node: NodeInfo,
        new_node: PageNode,
    ):
        pass

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
        logger.info(f"New node added with data: {node_info}")

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
        logger.info(f"New edge added with data: {edge_info}")
