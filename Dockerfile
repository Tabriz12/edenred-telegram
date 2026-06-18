FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    EDENRED_WEBHOOK_LISTEN=0.0.0.0 \
    EDENRED_WEBHOOK_PORT=8080

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY edenred_telegram ./edenred_telegram
COPY settings.toml ./
RUN uv sync --frozen --no-dev

RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

EXPOSE 8080

CMD ["/app/.venv/bin/edenred-telegram"]
