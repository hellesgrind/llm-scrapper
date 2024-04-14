import json
from typing import Dict, List

from data_manager import DataManager
from llm_client import OpenAIModel
from logs import logger
from parser import Page
from prompts import scrape_page_prompt
from schema import (
    PageNode,
    PageEdge,
    PageGraph,
)


class ResponseProcessor:

    def process(self, response: str, page_data: Page) -> PageGraph:
        logger.info(f"Start processing response")
        logger.debug(f"{response}")
        response_data = json.loads(response)
        nodes = self.create_nodes(
            response_data=response_data,
            page_data=page_data,
        )
        edges = self.create_edges(
            response_data=response_data,
            page_data=page_data,
        )
        logger.info("Finish processing response")
        return PageGraph(nodes=nodes, edges=edges)

    @staticmethod
    def create_nodes(
        response_data: Dict,
        page_data: Page,
    ) -> List[PageNode]:
        nodes: List[PageNode] = []
        nodes_data = response_data.get("nodes", [])
        if not nodes_data:
            logger.warning(
                f"Unable to get 'nodes' from response: {response_data}",
            )
            return nodes
        for data in nodes_data:
            temp_id = data.pop("temp_id", None)
            node_type = data.pop("node_type", None)
            if not temp_id or not node_type:
                logger.warning(
                    f"Unable to get 'temp_id' or 'node_type' of node: {data}"
                )
                continue
            node = PageNode(
                temp_id=temp_id,
                node_type=node_type,
                properties=data,
                source=page_data.url,
            )
            nodes.append(node)
        return nodes

    @staticmethod
    def create_edges(
        response_data: Dict,
        page_data: Page,
    ) -> List[PageEdge]:
        edges: List[PageEdge] = []
        edges_data = response_data.get("relationships", [])
        if not edges_data:
            logger.warning(
                f"Unable to get 'edges' from response: {response_data}",
            )
            return edges
        for data in edges_data:
            from_temp_id = data.pop("from_temp_id", None)
            to_temp_id = data.pop("to_temp_id", None)
            if not from_temp_id or not to_temp_id:
                logger.warning(
                    f"Unable to get 'from_temp_id' "
                    f"or 'from_temp_id' of edge: {data}"
                )
                continue
            edge = PageEdge(
                from_temp_id=from_temp_id,
                to_temp_id=to_temp_id,
                source=page_data.url,
            )
            edges.append(edge)
        return edges


class PageScrapper:
    def __init__(
        self,
        model: OpenAIModel,
        scrapper_schemas: List[Dict],
    ):
        self.model = model
        self.scrapper_schemas = scrapper_schemas
        self.response_processor = ResponseProcessor()

    async def scrape_page(self, page: Page) -> PageGraph:
        logger.info(f"Start scrapping page: {page.url}")
        page_text = page.body_text
        messages = [
            {
                "role": "user",
                "content": scrape_page_prompt(
                    page_text=page_text, scrapper_schemas=self.scrapper_schemas
                ),
            },
        ]
        response = await self.model.generate(messages)
        response_data = self.response_processor.process(
            response=response, page_data=page
        )
        logger.info(f"Scrapped page: {page.url}\n{response_data}")
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
        logger.info(
            f"ScrapperPipeline start. Scrapping schemas: {scrapper_schemas}",
        )

    async def run(self, url: str):
        page = await Page.parse(url)
        response_data = await self.scrapper.scrape_page(page)
        await self.data_manager.insert_data(response_data)
