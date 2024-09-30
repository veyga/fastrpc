import shutil
from pathlib import Path
from _fastrpc.server.utils.log import logger
from _fastrpc.server.codegen import server, client

SERVER_OUT = "__fastrpc_server__"


def transform_source(
    source_root: Path,
    client_out: Path,
) -> None:
    """
    Resolves + transforms all @fastrpc decorated definitions from a source root.
    """
    logger.info("Transforming sources...")
    if client_out.exists():
        logger.debug("Deleting generated client sources..")
        shutil.rmtree(client_out)
    if (server_out := source_root / SERVER_OUT).exists():
        logger.debug("Deleting generated server sources..")
        # shutil.rmtree(server_out)
        # (server_out / "__init__.py").touch()
    server.source_to_server(source_root, server_out)
    client.source_to_client(source_root, client_out)
    logger.info(f"Codegen complete")


__all__ = [
    "transform_source",
]
