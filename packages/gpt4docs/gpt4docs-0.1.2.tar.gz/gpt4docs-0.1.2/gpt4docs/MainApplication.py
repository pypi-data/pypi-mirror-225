import asyncio
import pdoc
import time
import os
from gpt4docs import ProjectManager, VectorStoreManager, LLMManager
from pathlib import Path
import argparse
import logging

logger = logging.getLogger(__name__)

pdoc.render.configure(docformat="google")


class MainApplication:
    def __init__(self, args):
        self._verify_args(args)
        self._verify_env()
        self.args = args

        if args.build:
            VectorStoreManager.build(args.vectorstore_path, args.project_path)

        self.project_manager = ProjectManager(args.project_path)
        self.vector_store_manager = VectorStoreManager(args.vectorstore_path)
        self.llm_manager = LLMManager(self.vector_store_manager.vectorstore)

    async def run(self):
        logger.info("Running")
        start = time.time()
        file_docstrings = await self.llm_manager.generate_docstrings(
            self.project_manager.get_files()
        )
        self.project_manager.update_docstrings(file_docstrings)

        logger.info(f"Finished. Time spent: {time.time() - start:.2f}s")
        new_root = self.project_manager.save()

        if self.args.compile:
            self.compile_docs(new_root)

    def compile_docs(self, new_root: str | Path):
        """Compile documentation using `pdoc`"""
        start = time.time()
        logger.info("Compiling documentation")
        pdoc.pdoc(new_root, output_directory=self.args.output_path)
        logger.info(f"Finished compiling. Time spent: {time.time() - start:.2f}s")

    def __call__(self, args: argparse.Namespace):
        if args.build:
            self.vector_store_manager.build(self.project_manager.project.project_root)
        else:
            asyncio.run(self.run())

    def _verify_args(self, args):
        if not args.project_path.exists():
            raise ValueError(f"Project path {args.project_path} does not exist")

        if not args.build and not VectorStoreManager.is_built(args.vectorstore_path):
            raise ValueError(
                "Vectorstore is not built. Run module with `--build` argument. "
                "`python3 -m gpt4docs --build ..."
            )

    def _verify_env(self):
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError(
                "OPENAI_API_KEY environment variable must be set to use LLM"
            )

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "project_path",
            type=Path,
            help="Path to root of project to write documentation for",
        )
        parser.add_argument(
            "vectorstore_path",
            type=Path,
            default=Path.cwd() / ".vectorstore",
            nargs="?",
            help="Path to vectorstore directory",
        )
        parser.add_argument(
            "--build",
            action="store_true",
            help="Build vectorstore",
        )
        parser.add_argument(
            "--compile",
            action="store_true",
            help="Compile documentation using pdoc",
        )
        parser.add_argument(
            "--output_path",
            default=Path.cwd() / "pdoc_output",
            help="Path to output documentation using pdoc",
        )
        args = parser.parse_args()

        logger.info(f"Arguments: {args}")
        return args
