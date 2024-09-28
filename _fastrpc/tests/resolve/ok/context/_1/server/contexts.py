from fastrpc import remote_procedure_type
from dataclasses import dataclass


@dataclass
class InvalidTokenException(Exception):
    msg: str


@remote_procedure_type
class TokenContext:
    token: str


def token_validator(context: TokenContext) -> None:
    if context.token != "valid":
        raise InvalidTokenException("invalid token was provided")
