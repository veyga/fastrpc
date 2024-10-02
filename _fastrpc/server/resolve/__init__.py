import importlib.machinery
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from fastapi import APIRouter


def build_router(source_root: Path) -> APIRouter:
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
    router = APIRouter()
    myechoers = import_module(f"api.myechoers")
    mymath = import_module(f"api.mymath")
    mystrings = import_module("api.mystrings")
    mystrings_ops = import_module("api.mystrings.ops")
    fastrpc_procedures = [
        myechoers.echo,
        mymath.add,
        mystrings.root_upper,
        mystrings_ops.upper,
        mystrings_ops.lower,
    ]
    for rpc in fastrpc_procedures:
        summary = f"{rpc.__module__}.{rpc.__name__}"
        path = summary.replace(".", "/")
        route = f"/{path}"
        description = f"{rpc.__doc__}"
        router.post(route, summary=summary, description=description)(rpc)
    return router


__all__ = [
    "build_router",
]
