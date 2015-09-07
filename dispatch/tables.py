# SQLAlchemy Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy import func
import datetime as dt
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Text
    )

Base = declarative_base()
default_time = dt.datetime(2001, 1, 1)

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime(True), default=func.now())
    _updated = Column(DateTime(True), default=func.now(), onupdate=func.now())
    _etag = Column(String(40))
    _id = Column(Integer, primary_key=True, autoincrement=True)

class Shifts(CommonColumns):
    __tablename__ = 'shifts';
    user_id = Column(Integer, ForeignKey('users._id'), nullable=False)
    state = Column(Enum('scheduled', 'in_progress', 'completed', name='shift_states'), default='scheduled')
    is_payed = Column(Boolean, default=0)
    scheduled_start = Column(DateTime(True))
    duration_in_minutes = Column(Integer, default=60)
    clock_in = Column(DateTime(True))
    clock_out = Column(DateTime(True), default=default_time)

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(user_id=data[0], is_payed=False, scheduled_start=func.now(), clock_in=func.now(), clock_out=default_time)

class Requests(CommonColumns):
    __tablename__ = 'requests'
    user_id = Column(Integer, ForeignKey('users._id'), nullable=False)
    delivery_location = Column(Text, nullable=False)
    need = Column(Text, nullable=False)
    notes = Column(Text)
    is_canceled = Column(Boolean, default=False)

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(user_id=data[0], delivery_location=data[1], need=data[2], notes=data[3], is_canceled=False)

class Deliveries(CommonColumns):
    __tablename__ = 'deliveries'
    request_id = Column(Integer, ForeignKey('requests._id'), nullable=False)
    sidekick_id = Column(Integer, ForeignKey('users._id'), nullable=False)
    in_progress = Column(DateTime(True))
    completed = Column(DateTime(True), default=default_time)
    is_canceled = Column(Boolean, default=False)

    def __init__(self, request_id, sidekick_id):
        self.request_id = request_id
        self.sidekick_id = sidekick_id
        self.in_progress = default_time
        self.completed = default_time
        self.is_canceled = False

    @classmethod
    def from_tuple(cls, data):
        """Helper method to populate the db"""
        return cls(request_id=data[0], sidekick_id=data[1])


class Users(CommonColumns):
    __tablename__ = 'users'
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    image = Column(Text, default='default.jpg')
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







