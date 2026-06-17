from pathlib import Path
from typing import Any

from dynaconf import Dynaconf

BASE_DIR = Path(__file__).resolve().parent.parent

settings = Dynaconf(
    envvar_prefix="EDENRED",
    environments=True,
    load_dotenv=True,
    settings_files=[
        BASE_DIR / "settings.toml",
        BASE_DIR / ".secrets.toml",
    ],
)

REQUIRED_SETTINGS = (
    "TELEGRAM_BOT_TOKEN",
    "WEBHOOK_URL",
)


def require_settings() -> Dynaconf:
    missing = [key for key in REQUIRED_SETTINGS if not settings.get(key)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Missing required settings: {names}")

    return settings


def optional_setting(name: str, default: Any = None) -> Any:
    value = settings.get(name, default)
    return default if value == "" else value
