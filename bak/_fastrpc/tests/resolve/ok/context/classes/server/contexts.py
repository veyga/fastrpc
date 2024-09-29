from fastrpc import remote_procedure_type


@remote_procedure_type
class Token:
    token: str


@remote_procedure_type
class Pagination:
    limit: int = 1
