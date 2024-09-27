from parametrization import Parametrization as P
from pathlib import Path
from _fastrpc.tests.conftest import case, Case


TEST_PATH = Path(__file__)


@P.autodetect_parameters()
@case("_1")
@case("_2")
@case("_3")
def test_ok(fix, run_resolve_test):
    run_resolve_test(Case.OK, TEST_PATH, fix)
