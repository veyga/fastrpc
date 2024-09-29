import pytest
from parametrization import Parametrization as P
from urllib.parse import urlencode
from .schema import Response
from . import PATH


@pytest.mark.asyncio
@P.autodetect_parameters()
@P.case(
    name="Echoes a single word",
    msg="echo",
)
@P.case(
    name="Echoes multiple words",
    msg="echo me",
)
async def test_echo(msg, test_client):
    params = urlencode({"message": msg})
    url = f"{PATH}/echo?{params}"
    response = test_client.get(url)
    assert test_client.is_ok(response.status_code)
    dct = response.json()
    Response.model_validate(dct)
    assert dct.get("message") == msg
