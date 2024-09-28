from fastrpc import remote_procedure_type


@remote_procedure_type
class TokenContext:
    token: str


def token_validator(context: TokenContext) -> None:
    assert context.token == "valid", "Invalid token"
