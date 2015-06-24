# SQLAlchemy Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    BLOB
    )

Base = declarative_base()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    id = Column(Integer, primary_key=True, autoincrement=True)

class Shifts(CommonColumns):
    __tablename__ = 'shifts';
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    state = Column(Enum('scheduled', 'in_progress', 'completed', name="shift_states"), default='scheduled')
    is_payed = Column(Boolean, default=0)
    scheduled_start = Column(DateTime)
    duration_in_minutes = Column(Integer, default=60)
    clock_in = Column(DateTime)
    clock_out = Column(DateTime)

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(user_id=data[0], is_payed=False, scheduled_start=func.now())


class Requests(CommonColumns):
    __tablename__ = 'requests'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    deliver_location = Column(String(120), nullable=False)
    need = Column(String(120), nullable=False)
    notes = Column(BLOB)
    is_canceled = Column(Boolean, default=False)

class Deliveries(CommonColumns):
    __tablename__ = 'deliveries'
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    sidekick_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    in_progress = Column(DateTime)
    completed = Column(DateTime)
    is_canceled = Column(Boolean, default=False)

class Users(CommonColumns):
    __tablename__ = 'users'
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    image = Column(String(240), default='default.jpg')
    has_vehicle = Column(Boolean)
    has_bike = Column(Boolean)
    type = Column(Enum('user', 'sidekick', 'arbitrator', 'admin', name='user_types'), default='user')
    is_suspended = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    requests = relationship(Requests, uselist=False, cascade="delete")
    deliveries = relationship(Deliveries, uselist=False)

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(first_name=data[0], last_name=data[1], email=data[2], phone=data[3], type=data[4], password="insertpasshere")







