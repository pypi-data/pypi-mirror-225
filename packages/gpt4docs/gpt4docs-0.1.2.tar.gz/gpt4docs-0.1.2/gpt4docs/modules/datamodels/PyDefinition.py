from typing import Optional
from pydantic import BaseModel
from enum import Enum


class PyDefinitionTypeEnum(str, Enum):
    function = "def"
    class_ = "class"


class PyDefinition(BaseModel):
    type: PyDefinitionTypeEnum
    name: str
    docstring: Optional[str] = None

    @property
    def full_docstring(self):
        value = self.docstring

        if value is None:
            return value

        if not value.startswith('"""'):
            value = '"""\n' + value
        if not value.endswith('"""'):
            value = value + '\n"""'

        return value
