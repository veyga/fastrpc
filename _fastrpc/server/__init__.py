import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pathlib import Path
from returns.result import Success, Failure, safe
from typing import Optional, Callable
from _fastrpc.server.resolve import build_router
from _fastrpc.server.exceptions import FastRPCException
from _fastrpc.server.utils.log import logger

type LifecycleOp = Optional[Callable[[FastAPI], None]]


def create_app(
    *,
    title: str,
    src_root: Path,
    client_out: Path,
    on_start: LifecycleOp = None,
    on_stop: LifecycleOp = None,
) -> FastAPI:
    """
    Creates a FastAPI application and generates the corresponding client library.

    This function initializes a FastAPI application with specific routes for
    OpenAPI documentation and handles the transformation of source code.

    ```python
    from fastrpc import FastRPC

    app = FastRPC.create(
      title="myapp",
      src_root=Path("/app/src"),
      client_out=Path("")
    )
    ```

    Args:
        title (str): The name of the FastAPI application.
        src_root (Path): Dir containing the source code to be transformed.
        client_out (Path): Directory to the generated client code will be stored.
        on_reload (fn): Function to run on app start [initial + every reload]
        on_stop (fn): Function to run on app stop [shutdown + before every reload]

    Returns:
        FastAPI: An instance of the FastAPI application.

    Raises:
        Exception: Any exceptions raised during the transformation of source code
        will propagate to the caller.
    """

    @safe
    def inner():
        def build(app: FastAPI):
            logger.info("Building application...")
            if client_out.exists():
                logger.info("Deleting generated client sources...")
                shutil.rmtree(client_out)
                logger.info("Existing client lib deleted")
            logger.info("Creating server components...")
            result = build_router(src_root)
            match result:
                case Success(router):
                    logger.info("Server components complete")
                    print(f"{router = }")
                    app.include_router(router)
                case Failure(e):
                    logger.error(e)
                    return

            logger.info("Creating client lib...")
            logger.info("Client lib complete")
            logger.info(f"fastrpc complete")

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            build(app)
            if on_start:
                on_start(app)
            yield
            if on_stop:
                on_stop(app)

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
            # TODO: do I need to catch here?
            # want a cleaner error message than printing a whole stack trace
            logger.error(e)
            raise e


__all__ = [
    "create_app",
]
