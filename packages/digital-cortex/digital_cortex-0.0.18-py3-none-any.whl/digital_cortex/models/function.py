from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class CodeType(str, Enum):
    file = "file"
    text = "text"


class DependencyType(str, Enum):
    file = "file"
    text = "text"


class FunctionForm(BaseModel):
    name: str
    engineId: str
    codeType: CodeType
    code: Optional[str] = None
    dependencyType: Optional[DependencyType] = None
    dependency: Optional[str] = None
    isPublished: bool


class UpdateFunctionCodeForm(BaseModel):
    id: str
    code: str


class UpdateDependencyForm(BaseModel):
    id: str
    dependencyType: DependencyType
    dependency: Optional[str] = None


class UpdateDescriptionForm(BaseModel):
    id: str
    description: str


class UpdateGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
    version: Optional[str] = None


class TagForm(BaseModel):
    id: str
    tagIds: List[str]
