from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CommandHandler, CallbackContext)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
import strings as s
from models import User, City
from utils import cities_keyboard, user_registered
from configuration import conf

# Menu stages
START, SETTINGS, FINISH = range(3)


default_markup = ReplyKeyboardMarkup(
    [
        [s.propose_new_event, s.events],
        [s.validate_event, s.menu],
    ],
    one_time_keyboard=True
)


@user_registered
def menu(update: Update, context: CallbackContext):
    menu_markup = ReplyKeyboardMarkup(
        [
            [s.feedback, s.faq],
            [s.update_city, s.main_menu],
        ],
        one_time_keyboard=True
    )
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.got_it,
                             reply_markup=menu_markup)
    return START


def update_city(update: Update, context: CallbackContext):
    reply_markup = InlineKeyboardMarkup(cities_keyboard())
    user = User.by(update.effective_user.id)
    update.effective_user.send_message(
        s.settings_update_city_intro % user.city.name, reply_markup=reply_markup)
    return FINISH


def finish_update_city(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    city_name = query.data.split(':')[1]
    city = City.by(name=city_name)
    if city:
        user = User.by(tg_id=query.from_user.id)
        user.update(city)

        query.edit_message_text(s.got_it)
        query.from_user.send_message(
            s.settings_update_city_done % user.city.name,
            reply_markup=default_markup)
    else:
        conf.logger.error("Unrecognized city: %s", city_name)

    return ConversationHandler.END


def faq(update: Update, context: CallbackContext):
    message = update.message
    message.from_user.send_message(
        s.faq_message,
        reply_markup=default_markup)

    return ConversationHandler.END


def feedback(update: Update, context: CallbackContext):
    message = update.message
    message.from_user.send_message(
        s.feedback_message,
        reply_markup=default_markup)

    return ConversationHandler.END


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.menu_unknown,
                             reply_markup=default_markup)
    return ConversationHandler.END


def main_menu(update: Update, context: CallbackContext):
    message = update.message
    message.from_user.send_message(
        s.got_it,
        reply_markup=default_markup)

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex('^%s$' % s.menu), menu)],
    states={
        START: [
            CallbackQueryHandler(menu, pattern='^menu$'),
            MessageHandler(Filters.regex('^%s$' % s.main_menu), main_menu),
            MessageHandler(Filters.regex('^%s$' % s.update_city), update_city),

            MessageHandler(Filters.regex('^%s$' % s.faq), faq),
            MessageHandler(Filters.regex('^%s$' % s.feedback), feedback),

        ],
        FINISH: [
            CallbackQueryHandler(finish_update_city,
                                 pattern='^select_city'),
        ],
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown),
    ]
)
