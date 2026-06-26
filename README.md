# edenred-telegram

Webhook-based Telegram bot skeleton that only accepts messages containing digits.

## Setup

Install dependencies:

```bash
uv sync
```

Set these environment variables:

```bash
EDENRED_TELEGRAM_BOT_TOKEN=123456789:replace-with-your-token
EDENRED_WEBHOOK_URL=https://example.com/telegram
EDENRED_TELEGRAM_WEBHOOK_SECRET_TOKEN=replace-with-a-random-secret
```

Runtime configuration is read from `EDENRED_*` environment variables. Optional
values use the defaults listed below when unset.

## Run

```bash
uv run edenred-telegram
```

The bot starts a webhook server using:

- `EDENRED_WEBHOOK_LISTEN` default `0.0.0.0`
- `EDENRED_WEBHOOK_PORT` default `8000`
- `EDENRED_WEBHOOK_URL` required, for example `https://example.com/telegram`
- `EDENRED_WEBHOOK_PATH` optional, defaults to the path in `EDENRED_WEBHOOK_URL`

## Docker

Build the image locally:

```bash
docker build -t edenred-telegram:local .
```

Run it with environment variables:

```bash
docker run --rm -p 8080:8080 \
  -e EDENRED_TELEGRAM_BOT_TOKEN=123456789:replace-with-your-token \
  -e EDENRED_WEBHOOK_URL=https://example.com/telegram \
  -e EDENRED_TELEGRAM_WEBHOOK_SECRET_TOKEN=replace-with-a-random-secret \
  edenred-telegram:local
```

The image listens on `0.0.0.0:8080` by default for Cloud Run compatibility.

## Deploy to Google Cloud Run

Create the runtime secrets:

```bash
gcloud secrets create telegram-bot-token --data-file=-
gcloud secrets create telegram-webhook-url --data-file=-
gcloud secrets create telegram-webhook-secret-token --data-file=-
```

Create the Artifact Registry Docker repository once:

```bash
gcloud artifacts repositories create cloud-run \
  --repository-format=docker \
  --location=europe-west1
```

Grant the Cloud Run runtime service account access to those secrets, then deploy
with Cloud Build:

```bash
gcloud builds submit \
  --config cloudbuild.yaml \
  --substitutions _REGION=europe-west1,_REPOSITORY=cloud-run,_SERVICE=edenred-telegram
```

## Behavior

- `/start` and `/help` explain that only digits are accepted.
- Text messages like `123456` are accepted.
- Any non-command text containing letters, punctuation, spaces between digits, or
  other non-digit characters is rejected.
