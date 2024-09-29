from fastapi import APIRouter
from .schema import Response
from . import RELATIVE_PATH

router = APIRouter(prefix=RELATIVE_PATH, tags=[])

METADATA = [
    {
        "name": RELATIVE_PATH,
        "description": """
          A friendly router 
        """,
    },
]


@router.get("/", response_description="Say hello")
async def say_hello() -> Response:
    return Response(message="hello")


@router.get("/echo", response_description="Echoes a message")
async def echo(message: str) -> Response:
    return Response(message=message)
