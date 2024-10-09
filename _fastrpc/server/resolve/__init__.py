import ast
import astor
from fastapi import APIRouter
import importlib.machinery
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from returns.result import safe, Success, Failure, ResultE
from _fastrpc.server.decorators import fastrpc_procedure
from _fastrpc.server.utils.log import logger
from _fastrpc.server.exceptions import FastRPCException


@safe
def build_router(source_root: Path) -> ResultE[APIRouter]:
    """
    Resolves, validates, and builds routes for all @fastrpc
    decorated definitions from a source root.
    """
    # src_root = Path("/Users/andrew.stefanich/Dev/python/tynacorp/src/api")
    # src_root = Path("/app/src/api")
    # spec = spec_from_file_location("myechoers", src_root)
    # TODO need to handle module import with "."
    # module = module_from_spec(spec)
    # module = importlib.machinery.SourceFileLoader(
    #     "myechoers",
    #     src_root.resolve().as_posix(),
    # ).load_module()
    # print(module.num)  # 42
    # print(module)

    # !!!!!!!
    # actually maybe don't need to import?
    # the resolver should return a list of modules

    # TODO resolve all routes
    # create an APIRouter, dynamically add routes
    # This function loops over fastrpc_procedures twice.

    p = Path("fastrpc/_fastrpc/server/resolve/mine.py")
    p.exists()
    with open(p, "r") as file:
        source_code = file.read()
        tree = ast.parse(source_code)
        logger.info(tree)
    print()
    router = APIRouter()
    myechoers = import_module(f"api.myechoers")
    mymath = import_module(f"api.mymath")
    mystrings = import_module("api.mystrings")
    mystrings_ops = import_module("api.mystrings.ops")
    fastrpc_procedures = (
        myechoers.echo,
        myechoers.echo_type,
        # myechoers.greet,
        # myechoers.myarg,
        # mymath.add,
        # mystrings.root_upper,
        # mystrings_ops.upper,
        # mystrings_ops.lower,
    )
    has_fail = False
    for rpc in fastrpc_procedures:
        logger.info(f"looking at {rpc.__name__}")
        summary = f"{rpc.__module__}.{rpc.__name__}"
        path = summary.replace(".", "/")
        route = f"/{path}"
        description = f"{rpc.__doc__}"
        try:
            router.post(route, summary=summary, description=description)(rpc)
            print("hey")
        except Exception as e:
            try:
                if "response_model=None" in (e.args[0]):
                    e.add_note("***NOTE: fastrpc disallows returning None")
            finally:
                logger.error(
                    f"Failed to construct route:\n{summary}: {e} {e.__notes__ or ''}"
                )

    if has_fail:
        raise FastRPCException("FAILED TO BUILD SERVER ROUTER")
    return router


__all__ = [
    "build_router",
]
