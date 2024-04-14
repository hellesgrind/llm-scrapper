from abc import ABC, abstractmethod
import os
from neo4j import AsyncGraphDatabase, AsyncSession

from schema import (
    NodeInfo,
    EdgeInfo,
)

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DB_NAME = os.getenv("NEO4J_DB_NAME")

neo4j_driver = AsyncGraphDatabase.driver(
    uri=NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    database=NEO4J_DB_NAME,
)


async def neo4j_session() -> AsyncSession:
    async with neo4j_driver.session() as session:
        yield session


# TODO: Implement 'search_entity'
class DatabaseIntegration(ABC):

    @abstractmethod
    def add_node(self, data):
        pass

    @abstractmethod
    def add_edge(self, data):
        pass

    @abstractmethod
    def get_all_nodes(self, node_type):
        pass


class Neo4jIntegration(DatabaseIntegration):
    add_node_query: str = """ 
    MERGE (n:{node_type} {{uuid: {uuid}, source: $source, {properties} }})
    """  # noqa: W291
    add_edge_query: str = """
    MATCH (f {{uuid: {fromUUID}}}), (t {{uuid: {toUUID}}})
    MERGE (f)-[:{edge_type} {{source: $edgeSource}}]-(t)
    """  # noqa: W291

    def __init__(
        self,
        db_session: AsyncSession,
    ):
        self.db_session = db_session

    async def add_node(self, node_info: NodeInfo):
        node_properties = []
        for property_name in node_info.properties.keys():
            node_properties.append(f"{property_name}: ${property_name}")
        node_properties = ", ".join(node_properties)
        query = self.add_node_query.format(
            node_type=node_info.type,
            uuid=f"'{node_info.uuid}'",
            properties=node_properties,
        )
        params = node_info.properties
        params["source"] = node_info.source
        await self.db_session.run(
            query=query,
            parameters=params,
        )

    async def add_edge(self, edge_info: EdgeInfo):
        query = self.add_edge_query.format(
            edge_type=edge_info.type,
            fromUUID=f"'{edge_info.from_uuid}'",
            toUUID=f"'{edge_info.to_uuid}'",
        )
        await self.db_session.run(
            query=query,
            parameters={
                "edgeSource": edge_info.source,
            },
        )

    def get_all_nodes(self, node_type):
        pass
