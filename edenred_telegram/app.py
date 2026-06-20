import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from edenred_telegram.config import get_setting, optional_setting, require_settings
from edenred_telegram.handlers import accept_digits, help_command, start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def build_application() -> Application:
    require_settings()

    application = Application.builder().token(get_setting("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, accept_digits)
    )

    return application


def main() -> None:
    require_settings()
    application = build_application()

    logger.info(
        "Starting bot with webhook on %s:%s%s%s",
        get_setting("WEBHOOK_LISTEN"),
        get_setting("WEBHOOK_PORT"),
        get_setting("WEBHOOK_PATH"),
        get_setting("WEBHOOK_URL"),
    )

    application.run_webhook(
        listen=get_setting("WEBHOOK_LISTEN"),
        port=int(get_setting("WEBHOOK_PORT")),
        url_path=get_setting("WEBHOOK_PATH"),
        webhook_url=get_setting("WEBHOOK_URL"),
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=bool(get_setting("DROP_PENDING_UPDATES")),
        secret_token=optional_setting("TELEGRAM_WEBHOOK_SECRET_TOKEN"),
    )
