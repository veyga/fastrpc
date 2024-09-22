_default:
  just --list

tests:
  pytest

dtests:
  python -m debugpy --listen 0.0.0.0:5680 --wait-for-client -m pytest

test TEST:
  pytest {{TEST}}

dtest TEST:
  python -m debugpy --listen 0.0.0.0:5680 --wait-for-client -m pytest {{TEST}}

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
