from enum import Enum

from pydantic import BaseModel
from typing import Optional, List


class UpdateTaskForm(BaseModel):
    id: str
    taskIds: List[str]


class UpdateGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
    version: Optional[str] = None
    domain: Optional[str] = None


class UpdateDescriptionForm(BaseModel):
    id: str
    description: str


class TagForm(BaseModel):
    id: str
    tagIds: List[str]


class RegexModelForm(BaseModel):
    name: str
    version: Optional[str] = None
    taskIds: List[str]
    domain: Optional[str] = None
    isPublished: bool


class Params(BaseModel):
    evalStrategy: str
    learningRate: float
    batchSize: int
    trainRatio: float
    epochs: int


class PyTorchModelForm(BaseModel):
    name: str
    version: Optional[str] = None
    taskIds: List[str]
    domain: Optional[str] = None
    baseModelId: str
    params: Params
    isPublished: bool


class UpdatePytorchModelForm(BaseModel):
    id: str
    baseModelId: str
    params: Params


class UrlType(str, Enum):
    HUGGING_FACE = "hugging_face"
    S3 = "s3"


class TrainedModelForm(BaseModel):
    name: str
    taskIds: List[str]
    domain: Optional[str] = None
    urlType: UrlType
    trainedUrl: str
    awsAccessKeyId: Optional[str] = None
    awsSecretAccessKey: Optional[str] = None
    version: Optional[str] = None
    isPublished: bool


class UpdateTrainedModelForm(BaseModel):
    id: str
    trainedUrl: str
    awsAccessKeyId: Optional[str] = None
    awsSecretAccessKey: Optional[str] = None
