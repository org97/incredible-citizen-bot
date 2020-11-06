# Невероятный Гражданин

Телеграм бот **Неверояный Гражданин** позваляет децентрализованным образом подавать идеи акций, валидирировать их, и участвовать.

Данный бот является реализацией идеи проекта [OIP-2](https://github.com/org97/OIPs/blob/main/OIPS/oip-2.md)

Отдельно взятая акция проходит через следующий жизненный цикл:

**Подача идеи акции**

Любой пользователь может подать идею, которая попадёт в пул идей для валидации.

**Валидация идеи акции**

Любой пользователь может провалидировать идею, оставив свои оценки. Лучшие идеи будут предложены для участия пользователям бота.

**Участие в акциях**

Пользователи в любой момент могут поучаствовать в лучших акциях, прошедвих необходимую валидацию.


## Как запустить бота локально

Скопируйте фаил `.env.example` в `.env` и заполните необходимые параметры.
Не забудьте изменить пароль `POSTGRES_PASSWORD`

Конфиграционный параметры логики бота могут быть изменены в файле `configuration.py`

### Запуск Docker контейнера с ботом и базой данных postgres

Убедитесь, что у вас установлен [Docker](https://www.docker.com)

Выполните команду 
```
docker-compose up --build
```

### Загрузка в базу городов Беларуси

В новом окне терминала выполните команду 
```
docker-compose exec incredible-citizen-bot python3 src/load_cities.py
```

После данного шага база данных будет подготовлена для работы бота. При последующих запусках бота загрузку городов выполнять не нужно (если только вы не удалите созданную папку `data` с фаилами базы данных)
