TEST_DESCRIPTION = "Duplicate names"

from fastrpc.server.decorators import remote_procedure
from fastrpc.server.exceptions import DuplicatedNameException

EXPECTED = DuplicatedNameException


@remote_procedure
def r3(): ...


@remote_procedure
def r3(): ...
