from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from menu import default_markup
from models import User, Event, City, Region
import strings as s
from datetime import datetime, timedelta
from configuration import conf
from utils import cities_keyboard, regions_keyboard, region_cities_keyboard, user_allowed

# New event stages
START, SELECTING_CITY, TYPING_NAME, TYPING_DATES, \
    TYPING_DESCRIPTION, REVIEW = range(6)


@user_allowed
def start_new_event(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(s.start_new_event_process_button,
                              callback_data='select_event_city')],
    ]
    update.message.reply_text(
        s.how_to_create_description,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return START


def select_event_city(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = User.by(query.from_user.id)
    if not user.can_create_new_events:
        query.from_user.send_message(s.events_limit_reached_error,
                                     reply_markup=default_markup)
        return ConversationHandler.END

    event_cities_keyboard = [
        [InlineKeyboardButton(
            user.city.name, callback_data='select_city:%s' % user.city.name)],
        [InlineKeyboardButton(
            "Города Беларуси >>", callback_data='select_city_2')],
        [InlineKeyboardButton(
            s.geo_independent_event, callback_data='select_city:None')],
    ]
    reply_markup = InlineKeyboardMarkup(event_cities_keyboard)

    if query.message.text == s.how_to_create_description:
        # on starting
        query.from_user.send_message(s.step1_select_event_city,
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=reply_markup)
    else:
        # on navigating back
        query.edit_message_text(s.step1_select_event_city,
                                parse_mode=ParseMode.HTML,
                                reply_markup=reply_markup)
    return SELECTING_CITY


def select_event_city_2(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    reply_markup = InlineKeyboardMarkup(regions_keyboard())
    query.edit_message_text(
        s.step1_select_event_city,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup)
    return SELECTING_CITY


def select_event_city_3(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    query.answer()

    region_name = query.data.split(':')[1]
    region = Region.by(name=region_name)
    reply_markup = InlineKeyboardMarkup(region_cities_keyboard(region=region))
    query.edit_message_text(
        s.step1_select_event_city,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup)
    return SELECTING_CITY


def enter_event_name(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # on stepping back there is no city name in query data
    if 'select_city' in query.data:
        city_name = query.data.split(':')[1]
        context.user_data['city_name'] = city_name

    keyboard = [
        [InlineKeyboardButton(s.step_back_button,
                              callback_data='select_event_city')],
    ]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.step2_event_name_description,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.typing_hint)
    return TYPING_NAME


def select_start_date(update: Update, context: CallbackContext):
    if update.message:
        # on specifying valid event name
        event_name = update.message.text
    elif update.edited_message:
        # on editing event name
        event_name = update.edited_message.text
    else:
        # on stepping back
        if update.callback_query:
            update.callback_query.answer()
        event_name = context.user_data['event_name']
    context.user_data['event_name'] = event_name

    if len(event_name) > conf.event_name_max_length:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=s.event_name_too_long_error)
        return TYPING_NAME

    keyboard = [
        [InlineKeyboardButton(s.step_back_button,
                              callback_data='enter_event_name')],
    ]
    example_date = (datetime.now() + timedelta(1)).replace(hour=17, minute=0)
    text = s.step31_select_event_start_date.format(
        example_date.strftime(conf.date_format))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return TYPING_DATES


def select_start_time(update: Update, context: CallbackContext):
    if update.message:
        # on specifying correct start date
        start_date_str = update.message.text
    elif update.edited_message:
        # on editing start date
        start_date_str = update.edited_message.text
    else:
        # on stepping back
        # TODO: on edit message there is an error
        update.callback_query.answer()
        start_date_str = context.user_data['start_date_str']
    context.user_data['start_date_str'] = start_date_str

    try:
        start_date = datetime.strptime(start_date_str, conf.date_format)
    except ValueError:
        # if user enters some invalid date like '30.02.2021 17:00'
        conf.logger.info('User entered invalid date: %s' % start_date_str)
        typing_dates_error(update, context)
        return TYPING_DATES

    # Check that start_date is within boundaries.
    # Note that we will not perform this check at the final step when
    # the event is actually submitted. It is in the interest of the user to satisfy
    # the lower boundary.
    diff_in_sec = (start_date - datetime.now()).total_seconds()
    diff_in_hours = divmod(diff_in_sec, 3600)[0]
    if diff_in_hours < conf.earliest_event_start_time_from_now:
        typing_dates_error(
            update, context, message=s.start_date_is_too_early_error)
        return TYPING_DATES
    elif diff_in_hours > conf.latest_event_start_time_from_now:
        typing_dates_error(
            update, context, message=s.start_date_is_too_late_error)
        return TYPING_DATES

    keyboard = [
        [InlineKeyboardButton(s.step_back_button,
                              callback_data='select_start_date')],
        [InlineKeyboardButton(s.skip,
                              callback_data='skip_start_time')],
    ]
    time_example = '01:30'
    text = s.step32_select_event_end_date.format(time_example)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return TYPING_DATES


def typing_dates_error(update: Update, context, message=s.typing_dates_error):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message)
    update.message = None
    select_start_date(update, context)
    return TYPING_DATES


def enter_event_description(update: Update, context: CallbackContext):
    if update.message:
        # on typing valid duration
        duration_str = update.message.text
    elif 'skip_start_time' in update.callback_query.data:
        # on skip duration time
        duration_str = None
        update.callback_query.answer()
    elif 'duration_str' in context.user_data:
        # on step back
        duration_str = context.user_data['duration_str']
        update.callback_query.answer()
    else:
        # fallback
        duration_str = None
    context.user_data['duration_str'] = duration_str

    keyboard = [
        [InlineKeyboardButton(s.step_back_button,
                              callback_data='select_start_date')],
    ]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.step4_event_description,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return TYPING_DESCRIPTION


def review_event(update: Update, context: CallbackContext):
    # only two cases should be possible here: handling message or edited message
    if update.message:
        context.user_data['event_description'] = update.message.text
    elif update.edited_message:
        context.user_data['event_description'] = update.message.text
    if len(context.user_data['event_description']) > conf.event_description_max_length:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=s.event_description_too_long_error)
        return TYPING_DESCRIPTION

    keyboard = [
        [InlineKeyboardButton(s.step_back_button,
                              callback_data='enter_event_description')],
        [InlineKeyboardButton(s.send_for_review,
                              callback_data='finish_event')],
    ]

    city = s.geo_independent_event if context.user_data[
        'city_name'] == 'None' else context.user_data['city_name']

    time = context.user_data['start_date_str']
    start_date = datetime.strptime(time, conf.date_format)
    end_date = start_date
    if context.user_data['duration_str']:
        hours, minutes = [int(x) for x in
                          context.user_data['duration_str'].split(':')]
        end_date += timedelta(hours=hours, minutes=minutes)
        time += ' - %s' % end_date.strftime(conf.date_format)

    review_message = s.step5_event_review_description.format(
        city,
        context.user_data['event_name'],
        time,
        context.user_data['event_description'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=review_message,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return REVIEW


def finish(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = User.by(query.from_user.id)
    city = City.by(context.user_data['city_name'])
    start_date = datetime.strptime(
        context.user_data['start_date_str'], conf.date_format)
    end_date = start_date
    if context.user_data['duration_str']:
        hours, minutes = [int(x) for x in
                          context.user_data['duration_str'].split(':')]
        end_date += timedelta(hours=hours, minutes=minutes)

    event = Event.create(creator=user,
                         city=city,
                         name=context.user_data['event_name'],
                         description=context.user_data['event_description'],
                         start_date=start_date,
                         end_date=end_date)

    query.from_user.send_message(
        s.thanks_for_event_creation_message,
        parse_mode=ParseMode.HTML,
        reply_markup=default_markup)
    return ConversationHandler.END


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.event_creation_process_interrupted_message)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex('^%s$' % s.propose_new_event), start_new_event)],
    states={
        START: [
            CallbackQueryHandler(
                select_event_city, pattern='^select_event_city$'),
        ],
        SELECTING_CITY: [
            # going back from the list of regional cities
            CallbackQueryHandler(select_event_city, pattern='^select_city_1$'),
            # selecting a region
            CallbackQueryHandler(select_event_city_2,
                                 pattern='^select_city_2$'),
            # selecting a city by region
            CallbackQueryHandler(select_event_city_3,
                                 pattern='^select_city_3'),
            # concrete city is selected
            CallbackQueryHandler(enter_event_name, pattern='^select_city'),
        ],
        TYPING_NAME: [
            # on going back from setting event name
            CallbackQueryHandler(select_event_city,
                                 pattern='^select_event_city$'),
            # on receiving event name
            MessageHandler(
                Filters.text & ~Filters.command, select_start_date
            )
        ],
        TYPING_DATES: [
            # on typing event start date
            MessageHandler(Filters.regex(
                r'^([0-2][0-9]|(3)[0-1])(\.)(((0)[0-9])|((1)[0-2]))(\.)20[0-9][0-9] ([0-1][0-9]|(2)[0-3]):([0-5][0-9])$'),
                select_start_time),
            # on going back from selecting date
            CallbackQueryHandler(enter_event_name,
                                 pattern='^enter_event_name$'),
            # on going back from selecting duration
            CallbackQueryHandler(select_start_date,
                                 pattern='^select_start_date$'),
            # on skippin selecting start time
            CallbackQueryHandler(enter_event_description,
                                 pattern='^skip_start_time$'),
            # on typing event duration
            MessageHandler(Filters.regex(
                r'^\d{2}:\d{2}$'), enter_event_description),
            # on invalid date/time format
            MessageHandler(Filters.text & ~Filters.command, typing_dates_error)
        ],
        TYPING_DESCRIPTION: [
            # on going back from typing description we restart TYPING_DATES process
            CallbackQueryHandler(select_start_date,
                                 pattern='^select_start_date$'),
            # on getting description
            MessageHandler(
                Filters.text & ~Filters.command, review_event
            )
        ],
        REVIEW: [
            CallbackQueryHandler(enter_event_description,
                                 pattern='^enter_event_description$'),
            CallbackQueryHandler(finish,
                                 pattern='^finish_event$'),
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown),
    ]
)
