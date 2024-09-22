TEST_DESCRIPTION = "Decorated non-async function"

from fastrpc.server.decorators import remote_procedure
from fastrpc.server.exceptions import SynchronousProcedureException

EXPECTED = SynchronousProcedureException


@remote_procedure
def r4(): ...
