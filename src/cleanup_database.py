from database import database as db
from models import Base


def main():
    Base.metadata.drop_all(bind=db.engine)


if __name__ == '__main__':
    main()
