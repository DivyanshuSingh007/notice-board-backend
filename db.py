from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Resolve database URL from environment, fallback to local SQLite
raw_database_url = os.getenv("DATABASE_URL", "sqlite:///./notice.db")

# Render/Heroku style URLs sometimes start with postgres://; SQLAlchemy expects postgresql+psycopg2://
if raw_database_url.startswith("postgres://"):
    raw_database_url = raw_database_url.replace("postgres://", "postgresql+psycopg2://", 1)

# Configure connect_args only for SQLite
connect_args = {"check_same_thread": False} if raw_database_url.startswith("sqlite") else {}

engine = create_engine(raw_database_url, connect_args=connect_args)

Sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

BASE = declarative_base()
