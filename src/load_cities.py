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
      - name: Брест
        region_id: 1
      - name: Барановичи
        region_id: 1
      - name: Белоозёрск
        region_id: 1
      - name: Берёза
        region_id: 1
        
      - name: Витебск
        region_id: 2
      - name: Барань
        region_id: 2
      - name: Браслав
        region_id: 2
      - name: Верхнедвинск
        region_id: 2
      
      - name: Гомель
        region_id: 3
      - name: Буда-Кошелёво
        region_id: 3
      - name: Василевичи
        region_id: 3
      - name: Ветка
        region_id: 3
      
      - name: Гродно
        region_id: 4
      - name: Берёзовка
        region_id: 4
      - name: Волковыск
        region_id: 4
      - name: Дятлово
        region_id: 4
      
      - name: Минск
        region_id: 5
      - name: Березино
        region_id: 5
      - name: Борисов
        region_id: 5
      - name: Вилейка
        region_id: 5
        
      - name: Могилёв
        region_id: 6
      - name: Бобруйск
        region_id: 6
      - name: Быхов
        region_id: 6
      - name: Горки
        region_id: 6
        
      - name: Другой
    """
    Base.metadata.create_all(db.engine)
    sqla_yaml_fixtures.load(Base, db.session, fixture)


if __name__ == '__main__':
    main()
