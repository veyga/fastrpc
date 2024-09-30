import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from importlib import import_module
from pathlib import Path
from returns.result import Success, Failure, safe
from typing import Optional, Callable
from _fastrpc.server.codegen import transform_source
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

        @asynccontextmanager
        async def lifespan(app: FastAPI):

            def include_fastrpc_server():
                mod = import_module("__fastrpc_server__")
                app.include_router(mod.router)

            transform_source(src_root, client_out)
            server_path = str(src_root)
            if not sys.path[0] == server_path:
                sys.path.insert(0, server_path)
                include_fastrpc_server()
                sys.path.pop(0)
            else:
                include_fastrpc_server()
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
