from tools.llm import send_llm_request
from schemas.summary import ResearchReport
from schemas.search import SearchResult
from prompts.synthesis_prompt import parse_summaries, SYSTEM_PROMPT
from pydantic import ValidationError
from logger.log_config import logger
async def summarize(search_results: list[SearchResult]):
    prompt = parse_summaries(search_results)
    for _ in range(3):
        try:
            response = await send_llm_request(prompt, SYSTEM_PROMPT)
            report = ResearchReport.model_validate_json(response)
            return report
        except ValidationError as e:
            logger.error(f"validation error {e}")
            continue
    raise RuntimeError("unexpected error. Stop")