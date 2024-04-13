from abc import ABC, abstractmethod
import os
from neo4j import GraphDatabase

from logs import logger

NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DB_NAME = os.getenv("NEO4J_DB_NAME")


# TODO: Implement 'search_entity' and
#  relationship ingestion
class DatabaseIntegration(ABC):

    @abstractmethod
    def add_entity(self, entity_type, data):
        pass

    @abstractmethod
    def get_entity(self, entity_type, entity_id):
        pass

    @abstractmethod
    def get_all_entities(self, entity_type):
        pass

    @abstractmethod
    def update_entity(self, entity_type, entity_id, data):
        pass

    @abstractmethod
    def delete_entity(self, entity_type, entity_id):
        pass


class Neo4jIntegration(DatabaseIntegration):
    def __init__(self):
        self.driver = GraphDatabase.driver(
            uri=NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
            database=NEO4J_DB_NAME,
        )
        self._test_connection()

    def _test_connection(self):
        with self.driver.session() as session:
            try:
                session.run("RETURN 1")
                logger.info("Neo4j database connected successfully!")
            except ValueError as ve:
                logger.error(f"Neo4j database: {ve}")
                raise

    def add_entity(self, entity_type, data):
        pass

    def get_entity(self, entity_type, entity_id):
        pass

    def get_all_entities(self, entity_type):
        pass

    def update_entity(self, entity_type, entity_id, data):
        pass

    def delete_entity(self, entity_type, entity_id):
        pass
