from telegram import InlineKeyboardButton
from models import User
from telegram.ext import ConversationHandler
from functools import wraps
import strings as s


def cities_keyboard():
    return [
        # TODO: сделать через подгрузку справочника из базы
        [InlineKeyboardButton(
            "Минск", callback_data='select_city:Минск')],
        [InlineKeyboardButton(
            "Брест", callback_data='select_city:Брест')],
        [InlineKeyboardButton(
            "Гродно", callback_data='select_city:Гродно')],
        [InlineKeyboardButton(
            "Витебск", callback_data='select_city:Витебск')],
        [InlineKeyboardButton(
            "Могилёв", callback_data='select_city:Могилёв')],
        [InlineKeyboardButton(
            "Гомель", callback_data='select_city:Гомель')],
        [InlineKeyboardButton(
            "Другой", callback_data='select_city:Другой')],
    ]


numbers_1_10 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣',
                '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


def user_registered(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        tg_id = update.effective_user.id
        user = User.by(tg_id=tg_id)
        if not user:
            update.effective_user.send_message(s.user_is_not_registered_error)
            return ConversationHandler.END
        return func(update, context, *args, **kwargs)
    return wrapped


def user_allowed(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        tg_id = update.effective_user.id
        user = User.by(tg_id=tg_id)
        if user:
            if user.is_blocked:
                update.effective_user.send_message(s.action_is_blocked_error)
                return ConversationHandler.END
        else:
            update.effective_user.send_message(s.user_is_not_registered_error)
            return ConversationHandler.END
        return func(update, context, *args, **kwargs)
    return wrapped