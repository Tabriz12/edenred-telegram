from telegram import Update
from telegram.ext import ContextTypes

from edenred_telegram.config import get_setting


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return

    await update.effective_message.reply_text(get_setting("START_REPLY"))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None:
        return

    await update.effective_message.reply_text(get_setting("HELP_REPLY"))


async def accept_digits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message is None or update.effective_message.text is None:
        return

    text = update.effective_message.text.strip()
    if text.isdecimal():
        await update.effective_message.reply_text(
            get_setting("DIGITS_ACCEPTED_REPLY").format(digits=text)
        )
        return

    await update.effective_message.reply_text(get_setting("DIGITS_REJECTED_REPLY"))
