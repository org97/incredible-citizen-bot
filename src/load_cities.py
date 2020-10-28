import sqla_yaml_fixtures
from database import database as db
from models import Base


def main():
    fixture = """
    - City:
      - name: Минск
      - name: Брест
      - name: Гродно
      - name: Витебск      
      - name: Могилёв
      - name: Гомель
      - name: Другой
    """
    Base.metadata.create_all(db.engine)
    sqla_yaml_fixtures.load(Base, db.session, fixture)


if __name__ == '__main__':
    main()
