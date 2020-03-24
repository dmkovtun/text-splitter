# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    String,
)

from .base import Base
from .json_serializable import JSONSerializable
from .mixins import MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin


class Files(Base, JSONSerializable, MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin):
    __tablename__ = "files"

    title = Column("title", String(1024), unique=True)
