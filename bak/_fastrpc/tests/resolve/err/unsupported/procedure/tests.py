from parametrization import Parametrization as P
from pathlib import Path
from _fastrpc.tests.conftest import case, Case


TEST_PATH = Path(__file__)


@P.autodetect_parameters()
@case("marker")
# @case("method")
# @case("nested")
@case("obscured")
@case("return_none/explicit")
@case("return_none/untyped")
@case("synchronous")
def test_unsupported_procedures(fix, run_resolve_test):
    run_resolve_test(Case.ERR, TEST_PATH, fix)
