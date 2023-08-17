from pydantic import BaseModel
from typing import Optional, List


class EtlPipelineForm(BaseModel):
    name: str
    pipelineTypeId: str
    sourceDatasetId: str
    targetDatasetId: str
    functionId: str
    isPublished: bool


class UpdateEtlPipelineForm(BaseModel):
    id: str
    sourceDatasetId: str
    targetDatasetId: str
    functionId: str


class TagForm(BaseModel):
    id: str
    tagIds: List[str]


class UpdateDescriptionForm(BaseModel):
    id: str
    description: str


class UpdateGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
