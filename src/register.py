from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CommandHandler,
    CallbackContext)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from models import User, City
from menu import default_markup
from configuration import conf
import strings as s
from utils import cities_keyboard


# Registration stages
START, FINISH = range(2)


def start(update: Update, context: CallbackContext):
    user = User.by(tg_id=update.message.from_user.id)
    if user:
        update.message.reply_text(
            s.welcome_back,
            reply_markup=default_markup
        )
        return FINISH
    else:
        keyboard = [
            [InlineKeyboardButton(s.register, callback_data='register')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            s.new_user_greeting,
            reply_markup=reply_markup
        )
        return START


def register(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    reply_markup = InlineKeyboardMarkup(cities_keyboard())
    user.send_message(
        s.select_your_city, reply_markup=reply_markup)
    return FINISH


def finish_registration(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    city_name = query.data.split(':')[1]
    city = City.by(name=city_name)
    if city:
        User.create(tg_id=query.from_user.id, city=city)

        query.edit_message_text(s.registration_complete)
        query.from_user.send_message(
            s.registration_complete_message,
            reply_markup=default_markup)
    else:
        conf.logger.error("Unrecognized city: %s", city_name)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START: [
            CallbackQueryHandler(register, pattern='^register$'),
        ],
        FINISH: [
            CallbackQueryHandler(finish_registration,
                                 pattern='^select_city'),
        ],
    },
    fallbacks=[CommandHandler('start', start)],
)
