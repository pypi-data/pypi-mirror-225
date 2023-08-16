import asyncio
import sys
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

        if not args.no_build and not args.no_docstring:
            VectorStoreManager.build(args.vectorstore_path, args.project_path)
        else:
            logger.warning(
                "Not building vectorstore. Any recent changes will not be used to generate documentation. If you want to build the vectorstore, run without `--no-build` argument."  # noqa: E501
            )

        self.project_manager = ProjectManager(args.project_path)
        self.vector_store_manager = VectorStoreManager(args.vectorstore_path)
        self.llm_manager = LLMManager(self.vector_store_manager)

    async def run(self):
        logger.info("Running")
        if not self.args.no_docstring:
            await self.generate_docstrings()

        new_root = self.project_manager.save()

        if not self.args.no_readme:
            VectorStoreManager.build(
                self.args.vectorstore_path.parent / ".vectorstore_commented", new_root
            )
            await self.generate_readme(new_root)

        if self.args.compile:
            self.compile_docs(new_root)

        logger.info("Finished")

    async def generate_docstrings(self):
        """Generate docstrings using LLM"""
        start = time.time()
        logger.info("Generating docstrings")
        file_docstrings = await self.llm_manager.generate_docstrings(
            self.project_manager.get_files()
        )
        self.project_manager.update_docstrings(file_docstrings)
        logger.info(
            f"Finished generating docstrings. Time spent: {time.time() - start:.2f}s"
        )

    async def generate_readme(self, project_dir: str | Path):
        """Generate README.md using LLM"""
        start = time.time()
        logger.info("Generating README.md")
        readme = await self.llm_manager.generate_readme()
        self.project_manager.add_readme(readme, project_dir)
        logger.info(
            f"Finished generating README. Time spent: {time.time() - start:.2f}s"
        )

    def compile_docs(self, new_root: str | Path):
        """Compile documentation using `pdoc`"""
        start = time.time()
        logger.info("Compiling documentation")
        pdoc.pdoc(new_root, output_directory=self.args.output_path)
        logger.info(f"Finished compiling. Time spent: {time.time() - start:.2f}s")

    def __call__(self):
        asyncio.run(self.run())

    def _verify_args(self, args):
        if not args.project_path.exists():
            raise ValueError(f"Project path {args.project_path} does not exist")

        if args.no_build and not VectorStoreManager.is_built(args.vectorstore_path):
            raise ValueError(
                "Vectorstore is not built. Run module without `--no-build` argument. "
                "`python3 -m gpt4docs --no-build ..."
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
            "--no-build",
            action="store_true",
            help="Don't build the vectorstore",
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
        parser.add_argument(
            "--no-readme",
            action="store_true",
            help="Do not generate README.md",
        )
        parser.add_argument(
            "--no-docstring",
            action="store_true",
            help="Do not generate docstrings",
        )

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        args = parser.parse_args()

        logger.info(f"Arguments: {args}")
        return args
