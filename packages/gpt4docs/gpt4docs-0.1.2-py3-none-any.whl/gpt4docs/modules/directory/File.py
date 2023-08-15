import re
import black
from typing import Dict
from pathlib import Path
from gpt4docs.modules.datamodels import PyDefinition
import logging

logger = logging.getLogger(__name__)


class File:
    """This class will scan a Python file and return all the functions
    and classes in it"""

    original_definitions: Dict[str, PyDefinition] = {}
    definitions: Dict[str, PyDefinition] = {}

    # Regex for finding functions or classes, and docstrings
    re_definitions = r"""(?P<definition>^.*\b(?P<type>def|class)\b (?P<name>\w*) *\(?.*?\)?[\s\S]*?:$)\n*( *\"{3}(?P<docstring>[\s\S]*?)\"{3}\n*)?"""  # noqa: E501

    # Regex for finding specific function and classes based on type and name
    re_specific_definition = (
        r"(?P<definition>^.*\b(?P<type>{type})\b (?P<name>{name}) *\(?.*?\)?[\s\S]*?:$)\n*"  # noqa: E501
        + r"( *\"\"\"(?P<docstring>[\s\S]*?)\"\"\"\n*)?"
    )

    def __init__(self, file_path: str | Path) -> None:
        """Initializes the Scanner with the file path"""
        if isinstance(file_path, str):
            file_path = Path(file_path)
        self.content = self._read_file(file_path)
        self.file_path = file_path

        self.original_definitions = self._scan_for_definitions()
        self.definitions = self.original_definitions

    def _read_file(self, file_path):
        """Read file and format with black8 before returning content"""

        with open(file_path, "r") as f:
            content = f.read()

        formatted_content = black.format_str(content, mode=black.FileMode())

        return formatted_content

    def _scan_for_definitions(self) -> None:
        """Scans the file for functions and classes and their definitions"""

        defs = {}

        # Create definitions from all matches
        for match in re.finditer(self.re_definitions, self.content, flags=re.MULTILINE):
            defs[match.group("name")] = PyDefinition(
                type=match.group("type"),
                name=match.group("name"),
                docstring=match.group("docstring"),
            )
        return defs

    def _handle_indentation(self, match, definition) -> str:
        # Indentation level is 4 spaces + any spaces before the definition
        indentation_level = 4
        indentation_level += len(re.search(r"^ *", match.group("definition")).group(0))

        # Apply indentation to full docstring (with quotations)
        indented_docstring = []
        for line in definition.full_docstring.split("\n"):
            # Line is empty (no indentation)
            if line.strip() == "":
                # Important to add empty line to avoid unwanted whitespaces
                indented_docstring.append("")
                continue

            # Line is already indented
            if line.startswith(" " * indentation_level):
                indented_docstring.append(line)
                continue

            # Line is not indented, but not empty. Indent it.
            indented_docstring.append(" " * indentation_level + line)

        return "\n".join(indented_docstring)

    def _write_docstring(self, lines: str, definition: PyDefinition) -> str:
        """Find the definition in the file and write the docstring from the
        pydefinition object"""
        if definition.docstring is None:
            return lines

        # Regex to find specific definition
        re_specific_def = self.re_specific_definition.format(
            type=definition.type, name=definition.name
        )

        # Match to find indentation level
        match = re.search(re_specific_def, lines, flags=re.MULTILINE)

        if match is None:
            logger.warning(
                f"Could not find definition {definition.name} in file {self.file_path}"
            )
            return lines

        indented_docstring = self._handle_indentation(match, definition)
        replacement = rf"\g<definition>\n{indented_docstring}\n"

        if match.group("type") == "class":
            replacement += "\n"

        new_code = re.sub(re_specific_def, replacement, lines, flags=re.MULTILINE)

        return new_code

    def set_docstring(self, name: str, docstring: str) -> None:
        """Set the definitions for a given function or class in the file"""
        self.definitions[name].docstring = docstring

    def set_definition(self, definition: PyDefinition) -> None:
        self.definitions[definition.name] = definition

    def save(self, path: Path = None, overwrite: bool = False) -> None:
        """Writes the new definitions to the file"""
        lines = self.content

        for definition in self.definitions.values():
            lines = self._write_docstring(lines, definition)

        if overwrite:
            path = self.file_path
        elif path is None:
            raise ValueError("Path must be specified if overwrite is False")

        with open(path, "w") as f:
            f.writelines(lines)

    def get_docs(self) -> Dict[str, PyDefinition]:
        return self.definitions.values()

    def get_original_docs(self) -> Dict[str, PyDefinition]:
        return self.original_definitions

    def __str__(self) -> str:
        pretty_definitions = "\n".join(
            [
                " " * 4 + f"{name}: {definition}"
                for name, definition in self.definitions.items()
            ]
        )
        return f"""File: {self.file_path}\nDefinitions:\n{pretty_definitions}"""
