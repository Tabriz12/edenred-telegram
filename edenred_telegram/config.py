from pathlib import Path
from typing import Any

from dynaconf import Dynaconf

BASE_DIR = Path(__file__).resolve().parent.parent
ENVVAR_PREFIX = "EDENRED"
SETTINGS_FILES = (
    BASE_DIR / "settings.toml",
    BASE_DIR / ".secrets.toml",
)

settings = Dynaconf(
    envvar_prefix=ENVVAR_PREFIX,
    environments=True,
    load_dotenv=True,
    settings_files=SETTINGS_FILES,
)

REQUIRED_SETTINGS = (
    "TELEGRAM_BOT_TOKEN",
    "WEBHOOK_URL",
)


def get_setting(name: str, default: Any = None) -> Any:
    """Read config through Dynaconf so EDENRED_* env vars override local files."""
    value = settings.get(name, default)
    return default if value == "" else value


def require_settings() -> Dynaconf:
    missing = [key for key in REQUIRED_SETTINGS if not get_setting(key)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Missing required settings: {names}")

    return settings


def optional_setting(name: str, default: Any = None) -> Any:
    return get_setting(name, default)
