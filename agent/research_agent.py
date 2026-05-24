from tools.search import search_web, SearchConfig
from tools.summary import summarize

async def research_agent(query: str):
    search_result = await search_web(query, SearchConfig())
    report = await summarize(search_result)
    return report
