# -*- coding: utf-8 -*-
from sqlalchemy import Column

from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from .base import Base
from .json_serializable import JSONSerializable
from .mixins import MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin


class SentencesInFiles(
    Base, JSONSerializable, MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin
):
    __tablename__ = "sentences_in_files"

    sentence_id = Column("sentence_id", BIGINT(unsigned=True))
    word_id = Column("file_id", BIGINT(unsigned=True))
    position = Column("position", INTEGER(unsigned=True))
