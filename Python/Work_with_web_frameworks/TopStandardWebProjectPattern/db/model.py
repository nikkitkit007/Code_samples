from sqlalchemy import (Column, DateTime,
                        Integer, String, Boolean, ForeignKey)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from config import WORK_SCHEMA


Base = declarative_base()


class WithID:
    id = Column(Integer(), primary_key=True, comment='Unique ID')


class CreatedUpdated:
    created = Column(DateTime(), server_default=func.now())
    updated = Column(DateTime(), server_default=func.now(), onupdate=func.now())


class ConfigMixin:
    __table_args__ = {'schema': WORK_SCHEMA}


class User(Base, WithID, ConfigMixin):
    __tablename__ = "user"
    __table_args__ = {**ConfigMixin.__table_args__, **{'comment': 'User of system'}}
    name = Column(String(), comment='Name')
    lastname = Column(String(), comment='Lastname')
    role = Column(Boolean(), comment='Users role')


class Model2(Base, WithID, ConfigMixin):
    __tablename__ = "emotion"
    __table_args__ = {**ConfigMixin.__table_args__, **{'comment': 'Emotions metrics'}}
    worker_id = Column(Integer(), ForeignKey(User.id, ondelete='CASCADE'), nullable=False, comment='Сборщик эмоций')
