from api.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://search-frontend-phi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     import asyncio
#     from tools.search import SearchConfig, search_web
#     from logger.log_config import logger

#     res = asyncio.run(search_web("cristiano ronaldo", SearchConfig()))
#     for r in res:
#         logger.info(r.model_dump())
