from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from src.api import PATH as api_path
from src.api.router import router as api_router, METADATA as api_router_metadata
from src.shared.log import Logger
import sys

logger = Logger.COLORED


def do_it():
    logger.debug("asdfasdfasdf")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if True:
        # this is for dogfooding.
        # until the fastrpc tool is published, need to do this
        f = Path(__file__).parent.parent.parent.parent
        sys.path.insert(0, str(f))
        print(sys.path)
        print("asdf")
        print("yo")
        app.include_router(api_router)
    do_it()
    yield


app = FastAPI(
    openapi_url=f"{api_path}/openapi.json",
    docs_url=f"{api_path}/docs",
    redoc_url=f"{api_path}/redoc",
    openapi_tags=[*api_router_metadata],
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}
