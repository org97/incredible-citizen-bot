from configuration import conf

# Регистрация
welcome_back = 'С возвращением!'
register = 'Регистрация'
new_user_greeting = '''
Добро пожаловать в телеграм-бот <b>“Невероятный Гражданин”!</b>

Бот создан для того, чтобы гражданам всей Беларуси было удобно объединяться в целях создания и участия в акциях по всей стране для проявления своей гражданской позиции.
Бот позволяет <b>децентрализованно подавать идеи и участвовать в акциях.</b>

Под акциями мы понимаем публичные общественно-политические действия, позволяющие высказать свою точку зрения, привлечь внимание к проблеме, поддержать других людей, защитить свои интересы и политические взгляды <b>мирным способом.</b>
Так как бот является децентрализованным, идеи акции подаются самими участниками и проходят предварительный процесс независимой проверки и оценки случайно выбранными зарегистрированными пользователями.

<b>Бот является анонимным:</b> при регистрации вы указываете только город проживания, чтобы иметь возможность участвовать в гео-зависимых акциях в вашем регионе.
Вы не можете видеть других участников бота, однако вы можете видеть количество зарегистрированных на акцию участников.

Добро пожаловать на сторону силы!
'''
select_your_city = 'Укажите свой город'
registration_complete = 'Регистрация завершена'
registration_complete_message = '''
Спасибо за регистрацию!
Теперь вы можете предлагать и участвовать в акциях.
<b>Ваш город:</b> {}
'''
action_is_blocked_error = 'Извините, данное действие для вас заблокировано.'
user_is_not_registered_error = 'Вам необходимо зарегистрироваться. Используйте команду /start'

# Меню
menu = '🛠 Меню'
feedback = '💌 Обратная связь'
how_does_it_work = '🤷‍♂️ Как это работает'
got_it = 'Принято!'
update_city = '🌐 Обновить свой город'
unknow_request = 'Извините, я не понимаю что вы хотите.'
back = '<< Назад'
how_does_it_work_description = '''
Чат-бот “Невероятный гражданин” позволяет

<b>Участвовать в акциях</b>
- Для поиска подходящей акции и участия в ней перейдите в раздел “Акции” и выберите одну из предложенных акций
- У вас может быть только одна активная акция до её завершения
- Вы можете участвовать в более чем одной акции в день, если эти акции проводятся в разные промежутки времени
- После завершения первой акции вы можете зарегистрироваться на следующую
- После завершения акции Бот попросит вас подтвердить ваше участие и оценить прошедшую акцию. Пожалуйста, отнеситесь ответственно к этому шагу: ваше мнение важно для усовершенствования бота и предварительной проверки будущих акций.

<b>Проверять и оценивать акции</b>
- Все акции подаются децентрализованно участниками бота и проходят проверку и оценку случайными пользователями
- Вам может прийти сообщение от бота с предложением проверки и оценки акции
- Вы можете отключить приглашения к проверке акций в любое время и включить обратно. Если вы отказались проверять и оценивать акции 3 раза, вам больше не будут приходить уведомления о проверке акций.
- Для проверки, есть ли у вас акции для оценки или для включения/отключения проверок акций перейдите в меню “Проверить и оценить идею акции”

<b>Подавать идеи акций</b>
- Акции может подавать любой зарегистрированный участник бота
- Для подачи идеи перейдите в раздел “Подать идею акции”
- Акции должны соответствовать следующим требованиям: определению понятия акции чат-бота “Невероятный Гражданин”, иметь понятное название и описание, иметь время начала и окончания, быть мирной/не призывать к насилию
- Ваша акция будет проверена случайными зарегистрированными пользователями
- Если ваша акция при проверке имеет более низкий рейтинг, чем другие поданные акции, она может быть не показана в общем выборе активных акций. В следующий раз попробуйте сделать её более привлекательной.
- Если ваша акция не прошла проверку и не соответствует правилам Чат-бота “Невероятный Гражданин”, вы будете заблокированы.
'''
feedback_intro = 'Введите ваше сообщение'
feedback_finish = 'Спасибо, мы приняли ваше сообщение'
settings_update_city_intro = '<b>Ваш город:</b> {}'
settings_update_city_select_new = 'Выберите новый город:'
settings_update_city_done = '<b>Ваш город:</b> {}'
menu_unknown = 'Вы вышли из меню'

# Подача идеи акции
propose_new_event = '✊ Подать идею акции'
start_new_event_process_button = 'Приступить'
how_to_create_description = '''
Если у вас есть идея для акции - вы в правильном месте! Подавайте идеи акций хоть каждый день, если эти акции помогают нам всем достигать поставленных целей!

При подаче акции обратите, пожалуйста, внимание, на следующие требования:
<b>Понятные название и описание акции</b>
- В описании есть вся необходимая информация для принятия решения: участвовать в данной акции или нет
- Акция мирная, не призывает к насилию
- Акция не является провокацией
- Акция соответствует целям бота “Невероятный гражданин” - чтобы гражданам всей Беларуси было удобно объединяться в целях создания и участия в акциях по всей стране для проявления своей гражданской позиции.

<b>Для подачи идеи акции вам необходимо будет пройти 5 шагов:</b>
<b>Шаг 1:</b> Выбор города проведения
(если акция может проходить вне зависимости от геолокации, выберите “Гео-независимая акция”)
<b>Шаг 2:</b> Название акции
Укажите краткое название акции, отражающее суть вашей идеи
<b>Шаг 3:</b> Время проведения
- Укажите дату и время проведения в указанном формате (дд.мм.гггг чч:мм). Дата и время акции должны быть не раньше, чем через 1 час после подачи идеи
- Продолжительность акции: укажите время продолжительности акции, если это имеет смысл. Если акция не имеет окончания, пропустите этот шаг.
<b>Шаг 4:</b> Описание акции
Опишите подробно суть акции. Постарайтесь ответить в описании на следующие вопросы:
Когда? Где? Что надо делать? Какие необходимы атрибуты? Необходима ли предварительная подготовка? Как вы оцениваете риски этой акции?
<b>Шаг 5:</b> Ревью
Проверьте введенные данные. Вы можете вернуться на шаг назад, чтобы изменить введенные данные.
Как только вы отправите акцию на рассмотрение, акция уйдет на проверку и оценку случайным зарегистрированным пользователям.
'''
geo_independent_event = 'Гео-независимая акция'
step1_select_event_city = '<b>Шаг 1 из 5:</b> Выберите город проведения акции'
step2_event_name_description = '<b>Шаг 2 из 5:</b> Укажите название акции'
step31_select_event_start_date = '''
<b>Шаг 3 из 5:</b> Укажите время начала акции
Введите дату и время <b>начала акции</b> в фотмате <b>дд.мм.гггг чч:мм</b>
<b>Например:</b> {}
'''
step32_select_event_end_date = '''
<b>Шаг 3 из 5:</b> Укажите продолжительность акции
Введите время <b>продолжительности акции</b> в <b>чч:мм</b>
<b>Например:</b> {}
❗️ это не время окончания акции, а её продолжительность
Вы можете не указывать продолжительность, если это имеет смысл.
'''
step4_event_description = '<b>Шаг 4 из 5:</b> Укажите подробное описание акции'
step5_event_review_description = '''
<b>Шаг 5 из 5:</b> Проверьте введённые данные

<b>Город:</b>
{}
<b>Название:</b>
{}
<b>Время проведения:</b>
{}
<b>Описание:</b>
{}
'''
skip = 'Пропустить'
step_back_button = 'Вернуться на предыдущий шаг'
send_for_review = 'Отправить на рассмотрение'
thanks_for_event_creation_message = '''
Спасибо! Ваша идея принята и будет проверена случайными гражданами, зарегистрированными в боте.
Вы можете подавать идеи акций каждый день! Мы создаем новое будущее <b>вместе</b>!
'''
event_creation_process_interrupted_message = 'Процесс создания акции прерван. Попробуйте ещё раз.'
events_limit_reached_error = 'Вы достигли лимита на подачу новых акций в день. Попробуйте, пожалуйста, завтра.'
typing_dates_error = 'Ошибка ввода даты/времени. Пожалуйста, введите время <b>начала акции</b> в фотмате <b>дд.мм.гггг чч:мм</b>.'
start_date_is_too_early_error = 'Дата старта акции должна быть хотя бы через %sч.' % conf.earliest_event_start_time_from_now
start_date_is_too_late_error = 'Дата старта акции должна быть не позднее чем через %sч.' % conf.latest_event_start_time_from_now
event_name_too_long_error = 'Название акции не должно превышать %s символов. Пожалуйста, повторите.' % conf.event_name_max_length
event_description_too_long_error = 'Описание акции не должно превышать %s символов. Пожалуйста, повторите.' % conf.event_name_max_length
typing_hint = '👇'

# Проверка и оценка идеи акции
validate_event = '🕵️‍♀️ Проверить и оценить идею акции'
how_to_validate_description = '''
Добро пожаловать в раздел оценок и проверок акций.
Это самый важный отдел телеграм-бота “Невероятный Гражданин”!
Здесь вы можете проверять идеи акций, поданные участниками бота. Именно ваш голос может стать решающим и помочь боту верно оценивать акции, предлагать эффективные идеи гражданам и отсеивать опасные или бесполезные.
'''
start_event_validation_button = 'Приступить'
over_validation_limit = 'Превышен лимит проверенных акций. Попробуйте завтра.'
no_available_events_for_validation = 'Извините, в данный момент нет акций для проверки. Попробуйте позже.'
event_description_format = '''
<b>Город:</b>
{}
<b>Название:</b>
{}
<b>Время проведения:</b>
{}
<b>Описание:</b>
{}
'''
event_short_description_format = '{}\n<b>Время:</b> {}'
call_to_violence_question = 'Призывает ли данная акция к насилию?'
yes_danger = '☠️ Да'
no_safe = '✅ Нет'
rate_event_quality_message = '''
Оцените качественную составляющую данной идеи от <b>0 до 10</b>. 
Примите во внимание следующие факторы:
- Понятные <b>название и описание</b> акции. В описании должна быть вся необходимая информация для принятия решения, участвовать в данной акции или нет.
- <b>Акция мирная</b>, не призывает к насилию
- Акция не является провокацией
- Акция соответствует целям платформы <b>“Невероятный гражданин”</b> - чтобы гражданам всей Беларуси было удобно <b>объединяться</b> в целях создания и участия в акциях по всей стране <b>для проявления своей гражданской позиции</b>.
'''
your_answer = '<b>Ваш ответ:</b> {}'
rate_event_interest_message = 'Оцените интерес данной идеи для вас лично от <b>0 до 10</b>.'
event_validation_process_interrupted_message = 'Процесс проверки прерван. Попробуйте ещё раз.'
event_validation_with_call_to_violence_review = '''
<b>Проверьте ваши ответы</b>
Призыв к насилию: ☠️ Да

Идеи акций призывающие к насилию не требуют дальнейшей проверки.
Спасибо, что помогаете выявить их!
'''
event_validation_review = '''
<b>Проверьте ваши ответы</b>
Призыв к насилию: ✅ Нет
Качество идеи: {}
Ваш личный интерес в идее: {}
'''
edit_replies = 'Исправить ответы'
all_good = 'Всё верно'
thanks_for_validation = 'Спасибо! Ваша проверка принята. Вы помогаете боту быть полезным и безопасным для наших граждан!'

# Акции (выбор, участие, ревью)
events = '👫 Акции'
no_events_to_pick = 'В данный момент нет акций для участия. Попробуйте, пожалуйста, позже.'
pick_event_message = '''
Перед вами список <b>акций с наилучшим рейтингом</b> после проверки другими участниками.

Вы можете выбрать любую понравившуюся акцию. Вы можете участвовать в разных акциях, но не одновременно.
И помните - только вместе мы можем построить <b>Cтрану для Жизни</b>.
'''
event_selection_process_interrupted_message = 'Процесс участия в акции прерван. Попробуйте ещё раз.'
confirm = 'Подтвердить'
cancel_participation = 'Отменить участие'
participation_canceled = '''
Участие в акции отменено.
Надеемся, в следующий раз у вас получится поучаствовать!
<b>Долбить, долбить, долбить!</b> ❤️ ✊✌
'''
pick_another_event = 'Выбрать другую акцию'
your_participation_confirmed = '''
Спасибо, ваше участие подтверждено.
Вы всегда можете посмотреть число подтвердившихся участников по текущей активной акции в разделе <b>Акции</b>.
'''
confirmed_participants = '<b>Участвуют:</b> {}'
did_you_participate = '''
Акция, на которую вы откликнулись завершена:
<b>Название:</b> {}
<b>Время проведения:</b> {}

Расскажите, пожалуйста, участвовали ли вы в данной акции? Нам важно ваше мнение, чтобы бот “Невероятный Гражданин" мог улучшать качество проверки идей акций. Ваш ответ является анонимным.
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
