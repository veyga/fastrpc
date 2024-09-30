from pathlib import Path
from _fastrpc.server.utils.log import logger


def source_to_server(source_root: Path, server_out: Path) -> None:
    logger.info(f"Generating server code...")
    server_out.mkdir(parents=True, exist_ok=True)
    logger.info(f"Server code generated [see {str(server_out)}]")
