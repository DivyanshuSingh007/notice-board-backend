from db import BASE
from sqlalchemy import Column, Integer, String, Boolean, Date, Time

class Users(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique = True)
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(String)
    hashed_password = Column(String)
    admin = Column(Boolean, default=False)

class Notice(BASE):
    __tablename__ = 'notice'

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String)
    description = Column(String)
    post_date = Column(Date)
    event_date = Column(Date, nullable=True)
    event_start_time = Column(Time, nullable=True)
    event_end_time = Column(Time, nullable=True)
    type = Column(String)
