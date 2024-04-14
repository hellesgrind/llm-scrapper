from fastapi import FastAPI, Depends
from neo4j import AsyncSession

from database import Neo4jIntegration, neo4j_session
from schema import ScrapperPayload
from llm_client import OpenAIModel
from scrapper import ScrapperPipeline
from data_manager import DataManager


app = FastAPI()

scrapper_model = OpenAIModel(model_name="gpt-3.5-turbo")


@app.post("/scrapper")
async def scrapper(
    payload: ScrapperPayload, db_session: AsyncSession = Depends(neo4j_session)
):
    db_integration = Neo4jIntegration(db_session=db_session)
    data_manager = DataManager(db_integration=db_integration)
    pipeline = ScrapperPipeline(
        model=scrapper_model,
        scrapper_schemas=payload.scrapper_schemas,
        data_manager=data_manager,
    )
    await pipeline.run(url=payload.url)
