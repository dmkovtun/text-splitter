# -*- coding: utf-8 -*-

from sqlalchemy import (
    Column,
    Integer,
)

from sqlalchemy.dialects.mysql import BIGINT, INTEGER

from .base import Base
from .json_serializable import JSONSerializable
from .mixins import MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin


class WordsInSentences(
    Base, JSONSerializable, MysqlIdMixin, MysqlStatusMixin, MysqlTimestampsMixin
):

    __tablename__ = "words_in_sentences"

    sentence_id = Column("sentence_id", BIGINT(unsigned=True))
    word_id = Column("word_id", BIGINT(unsigned=True))
    position = Column("position", INTEGER(unsigned=True))
