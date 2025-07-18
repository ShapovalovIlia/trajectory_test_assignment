FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR app/

FROM base AS builder

COPY ./src ./src
COPY ./pyproject.toml ./pyproject.toml

RUN pip install build && \
    python3 -m build --wheel

FROM base AS runner

COPY --from=builder ./app/dist ./
RUN pip install trajectory*.whl

ENTRYPOINT trajectory

CMD ["--help"]
