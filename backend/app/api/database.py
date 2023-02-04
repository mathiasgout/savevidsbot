from api import config

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_INI_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "database.ini"
)

db_config = config.get_db_config(filename=DATABASE_INI_PATH, section="postgresql")


def create_sqlalchemy_engine(db_config):
    engine = create_engine(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )  # , echo=True)
    return engine


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_sqlalchemy_engine(db_config=db_config),
)

Base = declarative_base()
