from fastapi import FastAPI
from logs import logger

from database import Neo4jIntegration
from schema import ScrapperPayload


app = FastAPI()

db_integration = Neo4jIntegration()


@app.post("/scrapper")
async def scrapper(payload: ScrapperPayload):
    logger.info(f"Received payload: {payload}")
