from gpt4docs.modules.directory import File, Project
from typing import Dict
from pathlib import Path


class ProjectManager:
    def __init__(self, project_path: str):
        self.project = Project(Path(project_path))

    def update_docstrings(self, all_docstrings: Dict[File, Dict]):
        for file, definitions in all_docstrings.items():
            for def_ in definitions:
                self.project.get_file(file).set_definition(def_)

    def save(self):
        return self.project.save()

    def get_files(self):
        return self.project.files.values()
