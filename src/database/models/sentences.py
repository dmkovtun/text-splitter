# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    String,
)


from .base import Base
from .json_serializable import JSONSerializable
from .mixins import MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin


class Sentences(Base, JSONSerializable, MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "sentences"

    # cannot be unique because of correct answer
    # will may be duplicate on first round
    title = Column("title", String(1024))
