from fastapi.routing import APIRouter
from agent.research_agent import research_agent
from schemas.response import ResponseModel
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/research", response_model=ResponseModel)
async def research(request: dict):
    query = request.get("prompt", "")
    response = await research_agent(query)
    return {
        "title": response.title,
        "summary": response.summary,
        "insights": [f"{s.claim} (Source: {s.source})" for s in response.insights],
        "citations": response.citations
    }
   

