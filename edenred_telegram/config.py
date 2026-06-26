import os
from urllib.parse import urlparse
from typing import Any

from logger import get_logger

ENVVAR_PREFIX = "EDENRED"

logger = get_logger(__name__)

DEFAULT_SETTINGS = {
    "WEBHOOK_LISTEN": "0.0.0.0",
    "WEBHOOK_PORT": 8000,
    "DROP_PENDING_UPDATES": True,
    "START_REPLY": "Send a message that contains digits only.",
    "HELP_REPLY": "Only digits are accepted. Example: 123456",
    "DIGITS_ACCEPTED_REPLY": "Accepted: {digits}",
    "DIGITS_REJECTED_REPLY": "Please send digits only.",
}

REQUIRED_SETTINGS = (
    "TELEGRAM_BOT_TOKEN",
    "WEBHOOK_URL",
    "TELEGRAM_WEBHOOK_SECRET_TOKEN",
)


def get_setting(name: str, default: Any = None) -> Any:
    value = os.getenv(f"{ENVVAR_PREFIX}_{name}")
    fallback = DEFAULT_SETTINGS.get(name, default)
    if value in (None, ""):
        return fallback

    if isinstance(fallback, bool):
        return value.lower() in {"1", "true", "yes", "on"}
    if isinstance(fallback, int):
        return int(value)

    return value


def require_settings() -> None:
    missing = [key for key in REQUIRED_SETTINGS if not get_setting(key)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Missing required settings: {names}")


def optional_setting(name: str, default: Any = None) -> Any:
    return get_setting(name, default)


def get_webhook_path() -> str:
    explicit_path = os.getenv(f"{ENVVAR_PREFIX}_WEBHOOK_PATH")
    if explicit_path not in (None, ""):
        return explicit_path.strip("/")

    webhook_url = get_setting("WEBHOOK_URL", "")
    return urlparse(webhook_url).path.strip("/")
