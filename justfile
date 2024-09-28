_default:
  just --list

# Run all test suites
tests:
  pytest

# run a test under _fastrpc/tests (no arg tests all)
test *TEST:
  pytest _fastrpc/tests/{{TEST}}

# test with -k flag
ktest ARG:
  pytest -k {{ARG}}

# test with -k flag
dktest ARG:
  python -m debugpy --listen 0.0.0.0:5680 --wait-for-client -m pytest -k {{ARG}}

# debug a test under _fastrpc/tests
dtest *TEST:
  python -m debugpy --listen 0.0.0.0:5680 --wait-for-client -m pytest _fastrpc/tests/{{TEST}}

dscript FILE:
  python -m debugpy --listen 0.0.0.0:5680 --wait-for-client {{FILE}}

# format the repo
format:
  poetry run ruff format

# lint the repo
lint:
  poetry run ruff check

# lint the repo (+ auto-fix)
lintfix:
  poetry run ruff check --fix
