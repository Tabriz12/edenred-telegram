# edenred-telegram

Webhook-based Telegram bot skeleton that only accepts messages containing digits.

## Setup

Install dependencies:

```bash
uv sync
```

Create local secrets from the example:

```bash
cp .secrets.toml.example .secrets.toml
```

Set these values in `.secrets.toml` or as environment variables:

```bash
EDENRED_TELEGRAM_BOT_TOKEN=123456789:replace-with-your-token
EDENRED_WEBHOOK_URL=https://example.com/telegram
EDENRED_TELEGRAM_WEBHOOK_SECRET_TOKEN=replace-with-a-random-secret
```

Public defaults live in `settings.toml`. Secrets are loaded from `.secrets.toml`,
`.env`, or `EDENRED_*` environment variables via Dynaconf.

## Run

```bash
uv run edenred-telegram
```

The bot starts a webhook server using:

- `EDENRED_WEBHOOK_LISTEN` default `0.0.0.0`
- `EDENRED_WEBHOOK_PORT` default `8000`
- `EDENRED_WEBHOOK_PATH` default `telegram`
- `EDENRED_WEBHOOK_URL` required, for example `https://example.com/telegram`

## Behavior

- `/start` and `/help` explain that only digits are accepted.
- Text messages like `123456` are accepted.
- Any non-command text containing letters, punctuation, spaces between digits, or
  other non-digit characters is rejected.
