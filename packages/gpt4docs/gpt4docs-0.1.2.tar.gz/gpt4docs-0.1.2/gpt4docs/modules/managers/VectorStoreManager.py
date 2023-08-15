from pathlib import Path

from pydantic import PathNotADirectoryError
from gpt4docs.scripts.build_vectorstore import build_vectorstore
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class VectorStoreManager:
    def __init__(self, vectorstore_path: str):
        self.dir = vectorstore_path
        self.vectorstore = self.load(self.dir)

    @staticmethod
    def build(vectorstore_path: str, documents_folder: str):
        build_vectorstore(
            persist_directory=vectorstore_path, documents_folder=documents_folder
        )

    @staticmethod
    def is_built(vectorstore_path: str):
        return Path(vectorstore_path).exists()

    def load(self, vectorstore_path: str):
        if not self.is_built(vectorstore_path):
            raise ValueError(f"Cannot find vectorstore in {vectorstore_path}")

        vectorstore = Chroma(
            collection_name="documents",
            persist_directory=str(vectorstore_path),
            embedding_function=OpenAIEmbeddings(),
        )
        return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 6})
