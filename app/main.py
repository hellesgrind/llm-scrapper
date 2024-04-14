from fastapi import FastAPI

from database import Neo4jIntegration
from schema import ScrapperPayload
from llm_client import OpenAIModel
from scrapper import ScrapperPipeline
from data_manager import DataManager


app = FastAPI()

db_integration = Neo4jIntegration()
scrapper_model = OpenAIModel(model_name="gpt-3.5-turbo")
data_manager = DataManager(db_integration=db_integration)


@app.post("/scrapper")
async def scrapper(payload: ScrapperPayload):
    pipeline = ScrapperPipeline(
        model=scrapper_model,
        scrapper_schemas=payload.scrapper_schemas,
        data_manager=data_manager,
    )
    await pipeline.run(url=payload.url)
