from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
from _fastrpc.server.asts import transform_source


class FastRPC:
    """
    FastRPC framework
    """

    @staticmethod
    def create_app(
        *,
        app_name: str,
        client_out: Path,
        src_root: Path,
    ) -> FastAPI:
        """
        Creates a FastAPI application and resulting client library.
        """

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            transform_source(src_root, client_out)
            yield

        return FastAPI(
            openapi_url=f"/{app_name}/openapi.json",
            docs_url=f"/{app_name}/docs",
            redoc_url=f"/{app_name}/redoc",
            lifespan=lifespan,
        )


__all__ = [
    "FastRPC",
]
