from fastrpc.server import create
from parametrization import Parametrization as P
from pathlib import Path


@P.autodetect_parameters()
@P.case(
    name="_1",
    fix="_1",
)
def test_codegen_ok(fix):
    source, expected, actual = (
        f"{fix}/source.py",
        f"{fix}/expected.py",
        f"{fix}/actual.py",
    )
    create(src_root=fix)
    assert Path(actual).exists()
    # with open(source, "r") as f_source, open(expected,)
