from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class Database:
    def __init__(self):
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        db = os.getenv('POSTGRES_DB')
        self.engine = create_engine(f'postgres://{user}:{password}@{host}:{port}/{db}',
                                    pool_size=20,
                                    echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


database = Database()
