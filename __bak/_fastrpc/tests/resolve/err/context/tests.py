from parametrization import Parametrization as P
from pathlib import Path
from _fastrpc.tests.conftest import case, Case


TEST_PATH = Path(__file__)


@P.autodetect_parameters()
@case("simple")
def test_context(fix, run_resolve_test):
    run_resolve_test(Case.ERR, TEST_PATH, fix)
