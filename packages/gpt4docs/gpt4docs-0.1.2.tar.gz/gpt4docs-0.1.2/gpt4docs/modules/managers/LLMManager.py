from gpt4docs.model import LLM
import asyncio
import logging

from gpt4docs.modules.directory import File
from typing import List

logger = logging.getLogger(__name__)


class LLMManager:
    def __init__(self, retriever):
        self.llm = LLM(model_name="gpt-3.5-turbo-16k", retriever=retriever)

    async def generate_docstrings(self, files: List[File]):
        all_docstrings = {}

        for file in files:
            logger.info(f"Generating docstrings in file: {file.file_path}")
            tasks = [
                self._generate_docstring(definition) for definition in file.get_docs()
            ]
            definitions = await asyncio.gather(*tasks)
            logger.debug(definitions)
            all_docstrings.update({file: definitions})

        logger.info("Finished generating docstrings")
        return all_docstrings

    async def _generate_docstring(self, definition):
        definition.docstring = await self.llm.arun(definition.name)
        return definition
