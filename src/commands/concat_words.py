# -*- coding: utf-8 -*-
import signal

from scrapy.utils.log import configure_logging
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from sqlalchemy.orm import Session

from helpers import mysql_connection_string
from .base_command import BaseCommand


class ConcatWords(BaseCommand):
    def __init__(self):
        super().__init__()
        self.engine = None
        self.session = None
        self.stopped = False

    def connect(self) -> None:
        """Connects to database and rabbitmq (optionally)"""
        self.db = Connection()

    def signal_handler(self, signal, frame) -> None:
        self.logger.info("received signal, exiting...")
        self.stopped = True

    def add_options(self, parser) -> None:
        super().add_options(parser)

    def run(self, args: list, opts: list) -> None:
        self.set_logger("CONCAT_WORDS", self.settings.get("LOG_LEVEL"))
        configure_logging()
        self.connect()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # your code here

        self.db.close()
