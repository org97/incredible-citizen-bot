from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from models import User, Event, Participation
import strings as s
from utils import numbers_1_10
from menu import default_markup
from utils import user_registered
from datetime import datetime

# Event stages
PICK, CONFIRM, CHECKOUT, RATE = range(4)


@user_registered
def poll_events(update: Update, context: CallbackContext):
    """
    Entry point for polling events.
    """
    user = User.by(update.effective_user.id)
    participation = Participation.active(user=user)
    if participation:
        if participation.event.end_date < datetime.now():
            keyboard = [
                [InlineKeyboardButton(s.no_participated,
                                      callback_data='did_not_participate'),
                 InlineKeyboardButton(s.yes_participated,
                                      callback_data='did_participate')],
            ]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=participation.html_checkout_question(),
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(keyboard))
            return CHECKOUT
        else:
            event = participation.event
            text = event.html_full_description() + '\n' + event.html_participants()
            keyboard = [
                [InlineKeyboardButton(s.cancel_participation,
                                      callback_data='cancel_participation')],
            ]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=text,
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(keyboard))
            return ConversationHandler.END

    # hard check on not more than 10 events for picking
    events = Event.get_top_validated_events(user=user)[:10]
    if not events:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=s.no_events_to_pick,
                                 reply_markup=default_markup)
        return ConversationHandler.END
    message = s.pick_event_message + '\n'
    for index, event in enumerate(events):
        message += '{} {}\n\n'.format(numbers_1_10[index],
                                      event.html_short_description())

    buttons_in_row = 5
    first_row_buttons = [
        InlineKeyboardButton(index + 1,
                             callback_data='pick_event:%s' % event.id) for index, event in enumerate(events[:buttons_in_row])
    ]
    secon_row_buttons = [
        InlineKeyboardButton(index + buttons_in_row + 1,
                             callback_data='pick_event:%s' % event.id) for index, event in enumerate(events[buttons_in_row:])
    ]
    keyboard = [first_row_buttons, secon_row_buttons]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return PICK


def pick_event(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    event_id = query.data.split(':')[1]
    event = Event.by(id=event_id)

    keyboard = [
        [InlineKeyboardButton(s.pick_another_event,
                              callback_data='pick_another_event')],
        [InlineKeyboardButton(s.confirm,
                              callback_data='confirm:%s' % event_id)],
    ]

    text = event.html_full_description() + '\n' + event.html_participants()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return CONFIRM


def confirm(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = User.by(tg_id=update.effective_user.id)
    event_id = query.data.split(':')[1]
    event = Event.by(id=event_id)

    Participation.create(participant=user, event=event)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.your_participation_confirmed,
                             parse_mode=ParseMode.HTML,
                             reply_markup=default_markup)
    return ConversationHandler.END


def cancel_participation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = User.by(tg_id=update.effective_user.id)
    Participation.delete_active(user=user)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.participation_canceled,
                             parse_mode=ParseMode.HTML,
                             reply_markup=default_markup)
    return ConversationHandler.END


def did_not_participate(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = User.by(update.effective_user.id)
    participation = Participation.active(user=user)
    participation.update(confirmation=False)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.thank_you_for_no,
                             parse_mode=ParseMode.HTML,
                             reply_markup=default_markup)
    return ConversationHandler.END


def did_participate(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton('0', callback_data='rate:0'),
            InlineKeyboardButton('1', callback_data='rate:1'),
            InlineKeyboardButton('2', callback_data='rate:2'),
            InlineKeyboardButton('3', callback_data='rate:3'),
            InlineKeyboardButton('4', callback_data='rate:4'),
            InlineKeyboardButton('5', callback_data='rate:5')
        ],
        [
            InlineKeyboardButton('6', callback_data='rate:6'),
            InlineKeyboardButton('7', callback_data='rate:7'),
            InlineKeyboardButton('8', callback_data='rate:8'),
            InlineKeyboardButton('9', callback_data='rate:9'),
            InlineKeyboardButton('10', callback_data='rate:10')
        ]
    ]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.rate_event,
                             parse_mode=ParseMode.HTML,
                             reply_markup=InlineKeyboardMarkup(keyboard))
    return RATE


def rate(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    success_rating = query.data.split(':')[1]
    user = User.by(update.effective_user.id)
    participation = Participation.active(user=user)
    participation.update(confirmation=True, success_rating=success_rating)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.thank_you_for_yes,
                             parse_mode=ParseMode.HTML,
                             reply_markup=default_markup)
    return ConversationHandler.END


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.event_selection_process_interrupted_message)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^%s$' % s.events), poll_events),
        CallbackQueryHandler(cancel_participation,
                             pattern='^cancel_participation$'),
    ],
    states={
        PICK: [
            CallbackQueryHandler(pick_event, pattern='^pick_event'),
        ],
        CONFIRM: [
            CallbackQueryHandler(poll_events, pattern='^pick_another_event$'),
            CallbackQueryHandler(confirm, pattern='^confirm'),
        ],
        CHECKOUT: [
            CallbackQueryHandler(did_not_participate,
                                 pattern='^did_not_participate$'),
            CallbackQueryHandler(did_participate, pattern='^did_participate$'),
        ],
        RATE: [
            # on rating event
            CallbackQueryHandler(rate, pattern='^rate'),
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown),
    ]
)
