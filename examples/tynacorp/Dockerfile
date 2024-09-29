# -----------------------------------------------------------------------------------
# ------------------------------------ Base -----------------------------------------
# -----------------------------------------------------------------------------------
FROM python:3.12.4-bookworm as builder
USER root
RUN apt update
RUN apt install -y ripgrep bat tree less curl wget gpg
RUN pip install poetry
COPY pyproject.toml poetry.* ./
ARG IS_LOCAL=false
RUN poetry export --without-hashes $(test "$IS_LOCAL" = "true" && echo --with dev) -o requirements.txt
RUN python -m venv /opt/venv && PATH="/opt/venv/bin:$PATH" pip3 install --requirement requirements.txt

# -----------------------------------------------------------------------------------
# ------------------------------------ Final ----------------------------------------
# -----------------------------------------------------------------------------------
FROM builder as final
ENV PATH="/opt/venv/bin:$PATH"
RUN mkdir /app
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
RUN rm pyproject.toml poetry.lock
ENV PYTHONPATH="/app/fastrc:${PYTHONPATH}"
ENV PATH="${PATH}:/app/bin"
