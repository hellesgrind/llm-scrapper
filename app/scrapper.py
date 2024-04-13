import json
from typing import Dict, List

from parser import Page
from llm_client import OpenAIModel
from logs import logger
from data_manager import DataManager
from prompts import scrape_page_prompt


class PageScrapper:
    def __init__(
        self,
        model: OpenAIModel,
        scrapper_schemas: List[Dict],
    ):
        self.model = model
        self.scrapper_schemas = scrapper_schemas

    async def scrape_page(self, page: Page) -> List[Dict]:
        page_text = page.body_text
        logger.info(page_text)
        logger.info(self.scrapper_schemas)
        messages = [
            {
                "role": "user",
                "content": scrape_page_prompt(
                    page_text=page_text, scrapper_schemas=self.scrapper_schemas
                ),
            },
        ]
        response_data = await self.model.generate(messages)
        response_data = json.loads(response_data)
        return response_data

    # TODO:
    async def get_relevant_subpages(self, page: Page) -> List[str]:
        pass


class ScrapperPipeline:
    def __init__(
        self,
        model: OpenAIModel,
        data_manager: DataManager,
        scrapper_schemas: List[Dict],
    ):
        self.pages: List[Page] | None = []
        self.data_manager = data_manager
        self.scrapper = PageScrapper(
            model=model,
            scrapper_schemas=scrapper_schemas,
        )

    async def run(self, url: str):
        page = await Page.parse(url)
        response_data = await self.scrapper.scrape_page(page)
        logger.info(response_data)
