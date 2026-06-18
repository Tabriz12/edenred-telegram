from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from edenred_telegram.config import optional_setting, require_settings
from edenred_telegram.handlers import accept_digits, help_command, start


def build_application() -> Application:
    app_settings = require_settings()

    application = (
        Application.builder().token(app_settings.get("TELEGRAM_BOT_TOKEN")).build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, accept_digits)
    )

    return application


def main() -> None:
    app_settings = require_settings()
    application = build_application()

    application.run_webhook(
        listen=app_settings.get("WEBHOOK_LISTEN"),
        port=int(app_settings.get("WEBHOOK_PORT")),
        url_path=app_settings.get("WEBHOOK_PATH"),
        webhook_url=app_settings.get("WEBHOOK_URL"),
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=bool(app_settings.get("DROP_PENDING_UPDATES")),
        secret_token=optional_setting("TELEGRAM_WEBHOOK_SECRET_TOKEN"),
    )
