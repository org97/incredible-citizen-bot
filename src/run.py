from telegram.ext import Updater, MessageHandler, Filters
import strings as s
import menu
import register
import new_event
import validate_event
import poll_events
import error_handler
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    API_KEY = os.getenv('API_KEY')
    updater = Updater(API_KEY, use_context=True)

    # Conversation Handlers

    updater.dispatcher.add_handler(menu.conv_handler)
    updater.dispatcher.add_handler(register.conv_handler)
    updater.dispatcher.add_handler(new_event.conv_handler)
    updater.dispatcher.add_handler(validate_event.conv_handler)
    updater.dispatcher.add_handler(poll_events.conv_handler)
    updater.dispatcher.add_error_handler(error_handler.error_handler)

    # Message Handlers
    # TODO: do we need it?
    updater.dispatcher.add_handler(
        MessageHandler(Filters.command, menu.unknown))

    # Start the Bot

    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
