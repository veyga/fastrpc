import pytest
from fastrpc.client import apply_context
from .client import double_it, triple_it, TokenContext


@pytest.mark.asyncio
async def test_em():
    print("_")
    fdoubled = await double_it(x=4)(TokenContext(token="invalid"))
    print(f"{fdoubled = }")

    use_token_context = apply_context(TokenContext("valid"))

    doubled = await use_token_context(double_it(x=4))
    print(f"{doubled = }")

    tripled = await use_token_context(triple_it(x=4))
    print(f"{tripled = }")
