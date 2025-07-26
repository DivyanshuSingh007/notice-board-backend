from db import Sessionlocal
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
