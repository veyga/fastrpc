import pytest
from fastrpc.client import apply_context
from .client import double_it, TokenContext


@pytest.mark.asyncio
async def test_em():
    print("_")
    future = double_it(x=4)(TokenContext(token="invalid"))
    doubled = await future
    print(f"{doubled = }")

    use_token_context = apply_context(TokenContext("valid"))
    doubled = await use_token_context(double_it(x=4))
    # tripled = await use_token_context(triple_it(x=4))
    print(f"{doubled = }")

    # tripled = await use_token_context(triple_it(x=4))
    # print(f"{tripled = }")
