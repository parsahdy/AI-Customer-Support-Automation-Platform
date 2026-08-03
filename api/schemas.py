from pydantic import BaseModel, ConfigDict
from datetime import datetime



class QACreate(BaseModel):
    question: str
    answer: str


class QAOut(BaseModel):
    question: str
    answer: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)