from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from models import User, Event, Validation
import strings as s
from menu import default_markup
from utils import user_allowed

# Validate event stages
START, REVIEW_CALL_TO_VIOLENCE, RATE_QUALITY, RATE_INTEREST, FINISH = range(5)


@user_allowed
def start_event_validation(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(s.start_event_validation_button,
                              callback_data='validate_no_call_to_violence')],
    ]
    update.message.reply_text(
        s.how_to_validate_description,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return START


def validate_no_call_to_violence(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = User.by(tg_id=query.from_user.id)

    # try to find a not finished validatoin
    validation = user.get_not_finished_validation()
    if not validation:
        # check if user can validate today
        if not user.can_validate_today:
            query.from_user.send_message(
                s.over_validation_limit, reply_markup=default_markup)
            return ConversationHandler.END

        # check if there are events for validation available
        event = user.pick_event_for_validation()
        if not event:
            query.from_user.send_message(
                s.no_available_events_for_validation, reply_markup=default_markup)
            return ConversationHandler.END

        validation = Validation.create(user, event)

    keyboard = [
        [InlineKeyboardButton(s.yes_danger,
                              callback_data='handle_call_to_violence'),
         InlineKeyboardButton(s.no_safe,
                              callback_data='rate_event_quality')],
    ]

    query.from_user.send_message(validation.event.html_full_description(),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode=ParseMode.HTML)
    query.from_user.send_message(
        s.call_to_violence_question, reply_markup=InlineKeyboardMarkup(keyboard))
    return REVIEW_CALL_TO_VIOLENCE


def handle_call_to_violence(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = User.by(tg_id=query.from_user.id)
    validation = user.get_not_finished_validation()
    validation.update(call_to_violence=True)

    query.from_user.send_message(s.your_answer.format(
        s.yes_danger), parse_mode=ParseMode.HTML)
    query.from_user.send_message(
        s.thanks_for_validation, reply_markup=default_markup)
    return ConversationHandler.END


def rate_event_quality(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton('0', callback_data='quality:0'),
            InlineKeyboardButton('1', callback_data='quality:1'),
            InlineKeyboardButton('2', callback_data='quality:2'),
            InlineKeyboardButton('3', callback_data='quality:3'),
            InlineKeyboardButton('4', callback_data='quality:4'),
            InlineKeyboardButton('5', callback_data='quality:5')
        ],
        [
            InlineKeyboardButton('6', callback_data='quality:6'),
            InlineKeyboardButton('7', callback_data='quality:7'),
            InlineKeyboardButton('8', callback_data='quality:8'),
            InlineKeyboardButton('9', callback_data='quality:9'),
            InlineKeyboardButton('10', callback_data='quality:10')
        ]
    ]
    query.from_user.send_message(s.your_answer.format(s.no_safe),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode=ParseMode.HTML)
    query.from_user.send_message(
        s.rate_event_quality_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML)
    return RATE_QUALITY


def rate_event_interest(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # remember quality rating
    quality_rating = int(query.data.split(':')[1])
    context.user_data['quality_rating'] = quality_rating

    keyboard = [
        [
            InlineKeyboardButton('0', callback_data='interest:0'),
            InlineKeyboardButton('1', callback_data='interest:1'),
            InlineKeyboardButton('2', callback_data='interest:2'),
            InlineKeyboardButton('3', callback_data='interest:3'),
            InlineKeyboardButton('4', callback_data='interest:4'),
            InlineKeyboardButton('5', callback_data='interest:5')
        ],
        [
            InlineKeyboardButton('6', callback_data='interest:6'),
            InlineKeyboardButton('7', callback_data='interest:7'),
            InlineKeyboardButton('8', callback_data='interest:8'),
            InlineKeyboardButton('9', callback_data='interest:9'),
            InlineKeyboardButton('10', callback_data='interest:10')
        ]
    ]
    query.from_user.send_message(s.your_answer.format(quality_rating),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode=ParseMode.HTML)
    query.from_user.send_message(
        s.rate_event_interest_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML)
    return RATE_INTEREST


def review(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    quality_rating = context.user_data['quality_rating']
    interest_rating = int(query.data.split(':')[1])
    context.user_data['interest_rating'] = interest_rating

    keyboard = [
        [InlineKeyboardButton(s.edit_replies, callback_data='edit_replies'),
         InlineKeyboardButton(s.all_good, callback_data='finish')]
    ]
    query.from_user.send_message(s.your_answer.format(interest_rating),
                                 reply_markup=ReplyKeyboardRemove(),
                                 parse_mode=ParseMode.HTML)
    query.from_user.send_message(
        s.event_validation_review.format(quality_rating, interest_rating),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML)
    return FINISH


def finish(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    quality_rating = context.user_data['quality_rating']
    interest_rating = context.user_data['interest_rating']

    user = User.by(tg_id=query.from_user.id)
    validation = user.get_not_finished_validation()
    validation.update(call_to_violence=False,
                      quality_rating=quality_rating,
                      interest_rating=interest_rating)

    query.from_user.send_message(
        s.thanks_for_validation, reply_markup=default_markup)
    return ConversationHandler.END


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=s.event_validation_process_interrupted_message,
                             reply_markup=default_markup)
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(
        Filters.regex('^%s$' % s.validate_event), start_event_validation)],
    states={
        START: [
            CallbackQueryHandler(validate_no_call_to_violence,
                                 pattern='^validate_no_call_to_violence$'),
        ],
        REVIEW_CALL_TO_VIOLENCE: [
            CallbackQueryHandler(handle_call_to_violence,
                                 pattern='^handle_call_to_violence$'),
            CallbackQueryHandler(rate_event_quality,
                                 pattern='^rate_event_quality$'),
        ],
        RATE_QUALITY: [
            CallbackQueryHandler(rate_event_interest, pattern='^quality'),
        ],
        RATE_INTEREST: [
            CallbackQueryHandler(review, pattern='^interest'),
        ],
        FINISH: [
            CallbackQueryHandler(
                validate_no_call_to_violence, pattern='^edit_replies$'),
            CallbackQueryHandler(finish, pattern='^finish$'),
        ]
    },
    fallbacks=[
        MessageHandler(Filters.text, unknown),
    ]
)
