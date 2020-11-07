from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CommandHandler,
    CallbackContext)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update, ParseMode
import strings as s
from models import User, City, Region, Feedback
from utils import (
    cities_keyboard,
    regions_keyboard,
    region_cities_keyboard,
    user_registered)
from configuration import conf
import os

# Menu stages
START, UPDATING_CITY, FEEDBACK = range(3)


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
            [s.feedback, s.how_does_it_work],
            [s.update_city, s.back],
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
    if update.message:
        # navigating here from the menu
        update.effective_user.send_message(
            s.settings_update_city_intro.format(user.city.name),
            parse_mode=ParseMode.HTML)
        update.effective_user.send_message(
            s.settings_update_city_select_new,
            reply_markup=reply_markup
        )
    else:
        # navigating here from the back button
        query = update.callback_query
        query.edit_message_text(
            s.settings_update_city_select_new,
            reply_markup=reply_markup)
    return UPDATING_CITY


def update_city_2(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    reply_markup = InlineKeyboardMarkup(regions_keyboard())
    query.edit_message_text(
        s.settings_update_city_select_new,
        reply_markup=reply_markup)
    return UPDATING_CITY


def update_city_3(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    region_name = query.data.split(':')[1]
    region = Region.by(name=region_name)
    reply_markup = InlineKeyboardMarkup(region_cities_keyboard(region=region))
    query.edit_message_text(
        s.settings_update_city_select_new,
        reply_markup=reply_markup)
    return UPDATING_CITY


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
            s.settings_update_city_done.format(user.city.name),
            parse_mode=ParseMode.HTML,
            reply_markup=default_markup)
    else:
        conf.logger.error("Unrecognized city in update city: %s", city_name)
    return ConversationHandler.END


def how_does_it_work(update: Update, context: CallbackContext):
    message = update.message
    message.from_user.send_message(
        s.how_does_it_work_description,
        reply_markup=default_markup)
    return ConversationHandler.END


def feedback(update: Update, context: CallbackContext):
    message = update.message
    message.from_user.send_message(
        s.feedback_intro,
        reply_markup=default_markup)
    return FEEDBACK


def feedback_receive(update: Update, context: CallbackContext):
    message = update.message
    user = User.by(tg_id=message.from_user.id)
    Feedback.create(user=user, message=message.text)

    FEEDBACK_CHAT_ID = os.getenv('FEEDBACK_CHAT_ID')
    feedback = f'{s.feedback}::{message.from_user.id}\n{message.text}'
    context.bot.send_message(chat_id=FEEDBACK_CHAT_ID, text=feedback)

    message.from_user.send_message(
        s.feedback_finish,
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
    entry_points=[MessageHandler(Filters.regex('^%s$' % s.menu), menu)],
    states={
        START: [
            CallbackQueryHandler(menu, pattern='^menu$'),
            MessageHandler(Filters.regex('^%s$' % s.back), main_menu),
            MessageHandler(Filters.regex('^%s$' % s.update_city), update_city),
            MessageHandler(Filters.regex('^%s$' %
                                         s.how_does_it_work), how_does_it_work),
            MessageHandler(Filters.regex('^%s$' % s.feedback), feedback),
        ],
        UPDATING_CITY: [
            # going back from the list of regional cities
            CallbackQueryHandler(update_city, pattern='^select_city_1$'),
            # selecting a region
            CallbackQueryHandler(update_city_2, pattern='^select_city_2$'),
            # selecting a city by region
            CallbackQueryHandler(update_city_3, pattern='^select_city_3'),
            # concrete city is selected
            CallbackQueryHandler(finish_update_city, pattern='^select_city'),
        ],
        FEEDBACK: [
            MessageHandler(Filters.text & ~Filters.command, feedback_receive),
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown),
    ]
)
