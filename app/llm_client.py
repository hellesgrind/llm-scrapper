import os
from openai import AsyncOpenAI
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)


class OpenAIModel:
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
    ):
        self.client: AsyncOpenAI = OPENAI_CLIENT
        self.model_name: str = model_name
        self.temperature: float = temperature

    # TODO: Proper typing
    async def generate(self, messages: List[Dict]) -> str:
        completions = await self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
        )
        return completions.choices[0].message.content
