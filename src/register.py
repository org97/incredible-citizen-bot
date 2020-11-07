from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CommandHandler,
    CallbackContext)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from models import User, City, Region
from menu import default_markup
from configuration import conf
import strings as s
from utils import cities_keyboard, regions_keyboard, region_cities_keyboard


# Registration stages
START, CITY_SELECTION = range(2)


def start(update: Update, context: CallbackContext):
    user = User.by(tg_id=update.message.from_user.id)
    if user:
        update.message.reply_text(
            s.welcome_back,
            reply_markup=default_markup
        )
        return ConversationHandler.END
    else:
        keyboard = [
            [InlineKeyboardButton(s.register, callback_data='select_city_1')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            s.new_user_greeting,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        return START


def select_city_1(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    reply_markup = InlineKeyboardMarkup(cities_keyboard())
    if query.message.text == s.select_your_city:
        # on navidating back
        query.edit_message_text(s.select_your_city, reply_markup=reply_markup)
    else:
        # on register button pressed
        user.send_message(s.select_your_city, reply_markup=reply_markup)
    return CITY_SELECTION


def select_city_2(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    reply_markup = InlineKeyboardMarkup(regions_keyboard())
    query.edit_message_text(s.select_your_city, reply_markup=reply_markup)
    return CITY_SELECTION


def select_city_3(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    region_name = query.data.split(':')[1]
    region = Region.by(name=region_name)
    reply_markup = InlineKeyboardMarkup(region_cities_keyboard(region=region))
    query.edit_message_text(s.select_your_city, reply_markup=reply_markup)
    return CITY_SELECTION


def finish_registration(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    city_name = query.data.split(':')[1]
    city = City.by(name=city_name)
    if city:
        User.create(tg_id=query.from_user.id, city=city)

        query.edit_message_text(s.registration_complete)
        query.from_user.send_message(
            s.registration_complete_message.format(city.name),
            parse_mode=ParseMode.HTML,
            reply_markup=default_markup)
    else:
        conf.logger.error("Unrecognized city: %s", city_name)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START: [
            CallbackQueryHandler(select_city_1, pattern='^select_city_1$'),
        ],
        CITY_SELECTION: [
            # going back from the list of regional cities
            CallbackQueryHandler(select_city_1, pattern='^select_city_1$'),
            # selecting a region
            CallbackQueryHandler(select_city_2, pattern='^select_city_2$'),
            # selecting a city by region
            CallbackQueryHandler(select_city_3, pattern='^select_city_3'),
            # concrete city is selected
            CallbackQueryHandler(finish_registration, pattern='^select_city'),
        ],
    },
    fallbacks=[CommandHandler('start', start)],
)
