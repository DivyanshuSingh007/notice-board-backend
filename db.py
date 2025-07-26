from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_DATABASE_URL = 'sqlite:///./notice.db'

engine = create_engine(SQL_DATABASE_URL, connect_args={"check_same_thread" : False})

Sessionlocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

BASE = declarative_base()
