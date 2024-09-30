from pathlib import Path
from _fastrpc.server.utils.log import logger


def source_to_server(source_root: Path, server_out: Path) -> None:
    logger.info(f"Generating server code...")
    logger.info(f"Server code generated [see {str(server_out)}]")
