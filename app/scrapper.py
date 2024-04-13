from typing import Dict

from parser import Page
from llm_client import OpenAIModel
from logs import logger


class PageScrapper:
    def __init__(
        self,
        model: OpenAIModel,
    ):
        self.model = model


class ScrapperPipeline:
    def __init__(
        self,
        model: OpenAIModel,
        scrapper_schema: Dict,
    ):
        self.model = model
        self.scrapper_schema = scrapper_schema

    async def run(self, url: str):
        page = await Page.parse(url)
        logger.info(page.body_text)
