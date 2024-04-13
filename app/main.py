from fastapi import FastAPI
from loguru import logger

from schema import ScrapperPayload

app = FastAPI()


@app.post("/scrapper")
async def scrapper(payload: ScrapperPayload):
    logger.info(f"Received payload: {payload}")
