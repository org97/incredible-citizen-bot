from configuration import conf

# Регистрация
welcome_back = 'С возвращением!'
register = 'Регистрация'
new_user_greeting = 'Добро пожаловать в телеграм-бот "Невероятный Гражданин"!'
select_your_city = 'Укажите свой город'
registration_complete = 'Регистрация завершена'
registration_complete_message = '''
Спасибо. Добро пожаловать на светлую сторону!
Теперь вы можете подавать акции.
'''
action_is_blocked_error = 'Извините, данное действие для вас заблокировано.'
user_is_not_registered_error = 'Вам необходимо зарегистрироваться. Используйте команду /start'

# Меню
menu = 'Меню'
invite_friends = 'Пригласить друзей'
feedback = 'Обратная связь'
faq = 'FAQ'
got_it = 'Принято!'
update_city = 'Обновить свой город'
unknow_request = 'Извините, я не понимаю на чём вы настаиваете.'
main_menu = 'Главное меню'
faq_message = 'Однажды здесь появится FAQ'
feedback_message = 'Я тебя услышал'

settings_update_city_intro = '''Ваш город: %s. 
Выберите новый:'''
settings_update_city_done = 'Вы переключили город на: %s'
menu_unknown = 'Вы вышли из меню'

# Подача идеи акции
propose_new_event = 'Подать идею акции'
start_new_event_process_button = 'Приступить'
how_to_create_description = 'Здесь будет красивое описание о том как создавать акции'
geo_independent_event = 'Гео-независимая акция'
step1_select_event_city = '<b>Шаг 1 из 5:</b> Выберете город проведения акции'
step2_event_name_description = '<b>Шаг 2 из 5:</b> Укажите название акции (до %s символов)' % conf.event_name_max_length
step31_select_event_start_date = '''
<b>Шаг 3 из 5:</b> Укажите время начала акции
Введите дату и время <b>начала акции</b> в фотмате <b>дд.мм.гггг чч:мм</b>
<b>Например:</b> {}
'''
step32_select_event_end_date = '''
<b>Шаг 3 из 5:</b> Укажите продолжительность акции
Введите <i>опциональное</i> время <b>продолжительности акции</b> в <b>чч:мм</b>
<b>Например:</b> {}
❗️ это не время окончания акции, а её продолжительность
Вы можете не указывать продолжительность, если это имеет смысл.
'''
step4_event_description = '<b>Шаг 4 из 5:</b> Укажите подробное описание акции (до %s символов)' % conf.event_description_max_length
step5_event_review_description = '''
<b>Шаг 5 из 5:</b> Проверьте введённые данные

<b>Город:</b> {}
<b>Название:</b> {}
<b>Время проведения:</b> {}
<b>Описание:</b> {}
'''
skip = 'Пропустить'
step_back_button = 'Вернуться на предыдущий шаг'
send_for_review = 'Отправить на рассмотрение'
thanks_for_event_creation_message = 'Спасибо! Ваша идея принята на рассмотрение.'
event_creation_process_interrupted_message = 'Процесс создания акции прерван. Попробуйте ещё раз.'
events_limit_reached_error = 'Вы достигли лимита на создание новых идей в день. Попробуйте, пожалуйста, завтра.'
typing_dates_error = 'Ошибка ввода даты/времени. Пожалуйста, повторите.'
start_date_is_too_early_error = 'Дата старта акции должна быть хотя бы через %sч.' % conf.earliest_event_start_time_from_now
start_date_is_too_late_error = 'Дата старта акции должны быть не позднее чем через %sч.' % conf.latest_event_start_time_from_now
event_name_too_long_error = 'Название акции не должно превышат %s символов. Пожалуйста, повторите.' % conf.event_name_max_length
event_description_too_long_error = 'Описание акции не должно превышат %s символов. Пожалуйста, повторите.' % conf.event_name_max_length

# Валидация идеи акции
validate_event = 'Валидировать идею акции'
how_to_validate_description = 'Здесь будет красивое описание о том как валидировать акции'
start_event_validation_button = 'Приступить'
over_validation_limit = 'Превышен лимит валидаций акций. Попробуйте завтра.'
no_available_events_for_validation = 'Извините, в данный момент нет акций для валидации. Попробуйте позже.'
event_description_format = '''
<b>Город:</b> {}
<b>Название:</b> {}
<b>Время проведения:</b> {}
<b>Описание:</b> {}
'''
event_short_description_format = '{}\n<b>Время:</b> {}'
call_to_violence_question = 'Призывает ли данная акция к насилию?'
yes_danger = '☠️ Да'
no_safe = '✅ Нет'
rate_event_quality_message = '''
Оцените качественную состовляющую данной идеи от <b>0 до 10</b>. 
Примите во внимание следующие факторы:
- Понятное название, короткое и полное описание акции
- В описании есть вся необходимая информация для принятия решения участвовать в данной акции или нет
- Грамотная речь
'''
your_answer = '<b>Ваш ответ:</b> {}'
rate_event_interest_message = 'Оцените интерес данной идеи для вас лично от <b>0 до 10</b>.'
event_validation_process_interrupted_message = 'Процесс валидации прерван. Попробуйте ещё раз.'
event_validation_review = '''
<b>Ревью ваших ответов</b>
Призыв к насилию: ✅ Нет
Качество идеи: {}
Ваш личный интерес в идее: {}
'''
edit_replies = 'Исправить ответы'
all_good = 'Всё верно'
thanks_for_validation = 'Спасибо! Ваша валидация принята.'

# Акции (выбор, участние, ревью)
events = 'Акции'
no_events_to_pick = 'В данный момент нет акций для участия. Попробуйте, пожалуйста, позже.'
pick_event_message = '''
Перед вами список <b>акций с найлучшим рейтингом</b> после валидации другими участниками.

Вы можете выбрать любую понравившуюся акцию. Вы можете участвовать в разных акциях, но не одновременно.
И помните - только вместе мы можем построить <b>Cтрану для Жизни</b>.

<b>Долбить, долбить, долбить!</b> ❤️ ✊✌
'''
event_selection_process_interrupted_message = 'Процесс участия в акции прерван. Попробуйте ещё раз.'
confirm = 'Подтвердить'
cancel_participation = 'Отменить участние'
participation_canceled = '''
Участние в акции отменено.
Надеемся, в следующий раз у вас получится поучаствовать!
<b>Долбить, долбить, долбить!</b> ❤️ ✊✌
'''
pick_another_event = 'Выбрать другую акцию'
your_participation_confirmed = '''
Спасибо, ваше участие подтверждено.
Вы всегда можете посмотреть число подтвердившихся участников по вашей акции в разделе <b>Акции</b>.
'''
confirmed_participants = '<b>Участвуют:</b> {}'
did_you_participate = '''
Акция на которую вы откликнулись завершена:
<b>Название:</b> {}
<b>Время проведения:</b> {}

Ответьте пожалуйста, вы участвовали в данной акции?
'''
no_participated = '💔 Нет'
yes_participated = '✊ Да'
thank_you_for_no = '''
Спасибо за ваш ответ.
Надеемся, в следующий раз у вас получится поучаствовать!
<b>Долбить, долбить, долбить!</b> ❤️ ✊✌
'''
rate_event = 'Оцените, пожалуйста, по вашему внутреннему ощущению, была ли данная акция успешной по шкале от <b>0 до 10</b>.'
thank_you_for_yes = 'Cпасибо, <b>вы невероятны!</b> ❤️ ✊✌'
