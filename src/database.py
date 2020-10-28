from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///mydb.sqlite',
                                    connect_args={'check_same_thread': False},
                                    echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


database = Database()
