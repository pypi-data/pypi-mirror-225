from pydantic import BaseModel


class TextScoringForm(BaseModel):
    text: str
    modelId: str
