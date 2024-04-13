from typing import (
    List,
    Dict,
)

from database import DatabaseIntegration


class DataManager:
    def __init__(
        self,
        db_integration: DatabaseIntegration,
    ):
        self.db = db_integration

    def insert(self, data: List[Dict]):
        pass
