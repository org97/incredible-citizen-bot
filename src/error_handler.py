from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ParseMode
from configuration import conf
import traceback
import html
import json
import os


# based on https://github.com/python-telegram-bot/python-telegram-bot/blob/264b2c9c72691c5937b80e84e061c52dd2d8861a/examples/errorhandlerbot.py


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    conf.logger.error(msg="Exception while handling an update: ",
                      exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb = ''.join(tb_list)

    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(),
                               indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb),
    )

    DEVELOPER_CHAT_ID = os.getenv('DEVELOPER_CHAT_ID')
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID,
                             text=message[:4096], parse_mode=ParseMode.HTML)
