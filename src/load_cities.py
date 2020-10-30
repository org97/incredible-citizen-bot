import sqla_yaml_fixtures
from database import database as db
from models import Base


def main():
    fixture = """
    - Region:      
      - name: Брестская обл.
      - name: Витебская обл.
      - name: Гомельская обл.
      - name: Гродненская обл.
      - name: Минская обл.
      - name: Могилёвская обл.
      
    - City:
      - name: Барановичи
        region_id: 1
      - name: Белоозёрск
        region_id: 1
      - name: Берёза
        region_id: 1
      - name: Брест
        region_id: 1
      - name: Высокое
        region_id: 1
      - name: Ганцевичи
        region_id: 1
      - name: Давид-Городок
        region_id: 1
      - name: Дрогичин
        region_id: 1
      - name: Жабинка
        region_id: 1
      - name: Иваново
        region_id: 1
      - name: Ивацевичи
        region_id: 1
      - name: Каменец
        region_id: 1
      - name: Кобрин
        region_id: 1
      - name: Коссово
        region_id: 1
      - name: Лунинец
        region_id: 1
      - name: Ляховичи
        region_id: 1
      - name: Малорита
        region_id: 1
      - name: Микашевичи
        region_id: 1
      - name: Пинск
        region_id: 1
      - name: Пружаны
        region_id: 1
      - name: Столин
        region_id: 1
        
      - name: Барань
        region_id: 2
      - name: Браслав
        region_id: 2
      - name: Верхнедвинск
        region_id: 2
      - name: Витебск
        region_id: 2
      - name: Глубокое
        region_id: 2
      - name: Городок
        region_id: 2
      - name: Дисна
        region_id: 2
      - name: Докшицы
        region_id: 2
      - name: Дубровно
        region_id: 2
      - name: Лепель
        region_id: 2
      - name: Миоры
        region_id: 2
      - name: Новолукомль
        region_id: 2
      - name: Новополоцк
        region_id: 2
      - name: Орша
        region_id: 2
      - name: Полоцк
        region_id: 2
      - name: Поставы
        region_id: 2
      - name: Сенно
        region_id: 2
      - name: Толочин
        region_id: 2
      - name: Чашники
        region_id: 2
      
      - name: Буда-Кошелёво
        region_id: 3
      - name: Василевичи
        region_id: 3
      - name: Ветка
        region_id: 3
      - name: Гомель
        region_id: 3
      - name: Добруш
        region_id: 3
      - name: Ельск
        region_id: 3
      - name: Житковичи
        region_id: 3
      - name: Жлобин
        region_id: 3
      - name: Калинковичи
        region_id: 3
      - name: Мозырь
        region_id: 3
      - name: Наровля
        region_id: 3
      - name: Петриков
        region_id: 3
      - name: Речица
        region_id: 3
      - name: Рогачёв
        region_id: 3
      - name: Светлогорск
        region_id: 3
      - name: Туров
        region_id: 3
      - name: Хойники
        region_id: 3
      - name: Чечерск
        region_id: 3
      
      - name: Берёзовка
        region_id: 4
      - name: Волковыск
        region_id: 4
      - name: Гродно
        region_id: 4
      - name: Дятлово
        region_id: 4
      - name: Ивье
        region_id: 4
      - name: Лида
        region_id: 4
      - name: Мосты
        region_id: 4
      - name: Новогрудок
        region_id: 4
      - name: Островец
        region_id: 4
      - name: Ошмяны
        region_id: 4
      - name: Свислочь
        region_id: 4
      - name: Скидель
        region_id: 4
      - name: Слоним
        region_id: 4
      - name: Сморгонь
        region_id: 4
      - name: Щучин
        region_id: 4
      
      - name: Березино
        region_id: 5
      - name: Борисов
        region_id: 5
      - name: Вилейка
        region_id: 5
      - name: Воложин
        region_id: 5
      - name: Дзержинск
        region_id: 5
      - name: Жодино
        region_id: 5
      - name: Заславль
        region_id: 5
      - name: Клецк
        region_id: 5
      - name: Копыль
        region_id: 5
      - name: Крупки
        region_id: 5
      - name: Логойск
        region_id: 5
      - name: Любань
        region_id: 5
      - name: Марьина Горка
        region_id: 5
      - name: Минск
        region_id: 5
      - name: Молодечно
        region_id: 5
      - name: Мядель
        region_id: 5
      - name: Несвиж
        region_id: 5
      - name: Слуцк
        region_id: 5
      - name: Смолевичи
        region_id: 5
      - name: Солигорск
        region_id: 5
      - name: Старые Дороги
        region_id: 5
      - name: Столбцы
        region_id: 5
      - name: Узда
        region_id: 5
      - name: Фаниполь
        region_id: 5
      - name: Червень
        region_id: 5
        
      - name: Белыничи
        region_id: 6
      - name: Бобруйск
        region_id: 6
      - name: Быхов
        region_id: 6
      - name: Горки
        region_id: 6
      - name: Кировск
        region_id: 6
      - name: Климовичи
        region_id: 6
      - name: Кличев
        region_id: 6
      - name: Костюковичи
        region_id: 6
      - name: Кричев
        region_id: 6
      - name: Круглое
        region_id: 6
      - name: Могилёв
        region_id: 6
      - name: Мстиславль
        region_id: 6
      - name: Осиповичи
        region_id: 6
      - name: Славгород
        region_id: 6
      - name: Чаусы
        region_id: 6
      - name: Чериков
        region_id: 6
      - name: Шклов
        region_id: 6
        
      - name: Другой
    """
    Base.metadata.create_all(db.engine)
    sqla_yaml_fixtures.load(Base, db.session, fixture)


if __name__ == '__main__':
    main()
