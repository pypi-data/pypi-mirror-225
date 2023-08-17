from typing import Optional, List
from enum import Enum
from pydantic import BaseModel


class DatasetUrlForm(BaseModel):
    name: str
    datasetTypeId: str
    filePath: str
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None
    fileDelimiter: Optional[str] = None
    isPublished: bool


class DataFlow(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class FileOn(str, Enum):
    LOCAL = "local"
    S3 = "s3"


class DatasetCloudFileForm(BaseModel):
    name: str
    datasetTypeId: str
    dataFlow: DataFlow
    fileOn: FileOn
    targetBucket: Optional[str] = None
    targetFolder: Optional[str] = None
    awsAccessKeyId: Optional[str] = None
    awsSecretAccessKey: Optional[str] = None
    filePath: Optional[str] = None
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None
    fileDelimiter: Optional[str] = None
    isPublished: bool


class DatasetLocalFileForm(BaseModel):
    name: str
    datasetTypeId: str
    fileDelimiter: str
    isPublished: bool


class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"


class DatabaseDatasetForm(BaseModel):
    name: str
    datasetTypeId: str
    dataFlow: DataFlow
    databaseType: DatabaseType
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None
    dbUrl: str
    dbName: str
    dbUserName: str
    dbPassword: str
    dbTableName: Optional[str] = None
    isPublished: bool


class TagForm(BaseModel):
    id: str
    tagIds: List[str]


class UpdateDatasetUrlForm(BaseModel):
    id: str
    filePath: str
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None
    fileDelimiter: Optional[str] = None


class UpdateDatasetCloudFileForm(BaseModel):
    id: str
    fileOn: FileOn
    targetBucket: Optional[str] = None
    targetFolder: Optional[str] = None
    awsAccessKayId: Optional[str] = None
    awsSecretAccessKey: Optional[str] = None
    filePath: Optional[str] = None
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None
    fileDelimiter: Optional[str] = None


class UpdateDatasetLocalFileForm(BaseModel):
    id: str
    fileDelimiter: str


class UpdateDatabaseDatasetForm(BaseModel):
    id: str
    dbUrl: str
    dbName: str
    dbUserName: str
    dbPassword: str
    dbTableName: Optional[str] = None
    idColumn: Optional[str] = None
    textColumn: Optional[str] = None


class UpdateGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
    version: Optional[str] = None


class UpdateDescriptionForm(BaseModel):
    id: str
    description: str


class DBInfo(BaseModel):
    dataFlow: DataFlow
    databaseType: DatabaseType
    dbUrl: str
    dbName: str
    dbUserName: str
    dbPassword: str
    idColumn: str
    textColumn: str
    dbTableName: str
