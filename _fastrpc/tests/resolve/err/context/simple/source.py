from fastrpc.server import remote_procedure, Context, ContextHandler
from typing import TypedDict


class MyContext(TypedDict):
    name: str


def my_context_handler(ctx: MyContext):
    print(ctx)


@remote_procedure()
async def rp_1() -> str:
    return ""
