from pydantic import BaseModel

class ResponseModel(BaseModel):
    title: str
    summary: str
    insights: list[str]
    citations: list[str]