"""Top-level package for gpt4docs."""

__author__ = """Simon Moe Sørensen"""
__email__ = "moe.simon@gmail.com"
__version__ = "0.1.2"

from gpt4docs.modules import ProjectManager, VectorStoreManager, LLMManager
from gpt4docs.modules.datamodels.PyDefinition import PyDefinition, PyDefinitionTypeEnum
from gpt4docs.modules.directory.File import File
from gpt4docs.modules.directory.Project import Project
from gpt4docs.model.LLM import LLM
from gpt4docs.MainApplication import MainApplication
