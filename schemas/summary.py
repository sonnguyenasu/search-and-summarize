from pydantic import BaseModel

class ResearchItem(BaseModel):
    claim: str
    source: str

class ResearchReport(BaseModel):
    title: str
    summary: str
    insights: list[ResearchItem]
    citations: list[str]