import os
from dataclasses import dataclass
from typing import Literal

from dotenv import load_dotenv
import httpx
from network.client import client
from logger.log_config import logger
from schemas.search import SearchResult

load_dotenv()


@dataclass
class SearchConfig:
    api: str = os.getenv("TAVILY_API")
    url: str = os.getenv("TAVILY_URL")
    depth: Literal["basic", "advanced"] = os.getenv("SEARCH_DEPTH", "basic")
    max_results: int = int(os.getenv("SEARCH_RESULTS", 5))
    max_retries: int = int(os.getenv("SEARCH_MAXRETRY", 3))


async def search_web(query: str, config: SearchConfig):
    for _ in range(config.max_retries):
        try:
            payload = {
                "api_key": config.api,
                "query": query,
                "depth": config.depth,
                "max_results": config.max_results
            }
        
            response = await client.post(config.url, json=payload)
            response.raise_for_status()
            data = response.json()
            results = []
            for item in data.get("results", []):
                result = SearchResult(
                    title=item.get("title"),
                    url=item.get("url"),
                    content=item.get("content"),
                )
                results.append(result)
            return results
        except httpx.TimeoutException as e:
            logger.error("Timeout. Retry in 1 second....")
            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status error {e}. Retry in 1 second....")
            continue
        except Exception as e:
            logger.error(f"Unexpected error {e}. Logout")
            break
    raise RuntimeError("Error. Cannot proceed search request")
