from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
from returns.result import Success, Failure, safe
from typing import final
from _fastrpc.server.codegen import transform_source
from _fastrpc.server.exceptions import FastRPCException
from _fastrpc.server.utils.log import logger


@final
class FastRPC:
    """
    The main entrypoint to use FastRPC.
    ## Example

    ```python
    from fastrpc import FastRPC

    app = FastRPC.create(
      title="myapp",
      src_root=Path("/app/src"),
      client_out=Path("")
    )
    ```
    """

    @staticmethod
    def create(
        *,
        title: str,
        src_root: Path,
        client_out: Path,
    ) -> FastAPI:
        """
        Creates a FastAPI application and generates the corresponding client library.

        This function initializes a FastAPI application with specific routes for
        OpenAPI documentation and handles the transformation of source code.

        Args:
            title (str): The name of the FastAPI application.
            src_root (Path): Dir containing the source code to be transformed.
            client_out (Path): Directory to the generated client code will be stored.

        Returns:
            FastAPI: An instance of the FastAPI application.

        Raises:
            Exception: Any exceptions raised during the transformation of source code
            will propagate to the caller.
        """

        @safe
        def inner():

            @asynccontextmanager
            async def lifespan(_: FastAPI):
                transform_source(src_root, client_out)
                yield

            if not src_root.exists():
                raise FastRPCException(f"src_root {src_root} does not exist!")
            return FastAPI(
                openapi_url=f"/{title}/openapi.json",
                docs_url=f"/{title}/swagger",
                redoc_url=f"/{title}/redoc",
                lifespan=lifespan,
            )

        match inner():
            case Success(api):
                return api
            case Failure(e):
                logger.error(e)
                raise e


__all__ = [
    "FastRPC",
]
