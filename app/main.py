from fastapi import FastAPI
from logs import logger

from database import Neo4jIntegration
from schema import ScrapperPayload
from llm_client import OpenAIModel
from scrapper import ScrapperPipeline


app = FastAPI()

db_integration = Neo4jIntegration()
scrapper_model = OpenAIModel(model_name="gpt-3.5-turbo")


@app.post("/scrapper")
async def scrapper(payload: ScrapperPayload):
    logger.info(payload.url)
    logger.info(payload.scrapper_schema)
    pipeline = ScrapperPipeline(
        model=scrapper_model,
        scrapper_schema=payload.scrapper_schema,
    )
    await pipeline.run(url=payload.url)
