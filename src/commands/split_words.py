# -*- coding: utf-8 -*-
import signal
import time
from os import path
from os.path import exists
from typing import Dict

from scrapy.utils.log import configure_logging

from database.connection import Connection
from database.models import Files, Sentences, SentencesInFiles, Words, WordsInSentences
from database.models.base import Base

from .base_command import BaseCommand


class SplitWords(BaseCommand):
    def __init__(self):
        super().__init__()
        self.db = None
        self.stopped = False
        self.cached_words: Dict[str, int] = {}
        self.cached_sentences: Dict[str, int] = {}

    def connect(self) -> None:
        """Connects to database and rabbitmq (optionally)"""
        self.db = Connection()

    def signal_handler(self, signal, frame) -> None:
        self.logger.info("received signal, exiting...")
        self.stopped = True

    def add_options(self, parser) -> None:
        super().add_options(parser)

    def run(self, args: list, opts: list) -> None:
        self.set_logger("SPLIT_WORDS", self.settings.get("LOG_LEVEL"))
        configure_logging()
        self.connect()

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # your code here
        for filename in args:
            filename = filename.replace("\\", "/")
            if path.exists(filename):

                self.db.insert({"title": filename}, Files)
                time.sleep(1)
                file_id = self.get_id(filename, Files)
                self.logger.info(file_id)
                with open(filename, "r") as opened_file:
                    for sentence_count, sentence in enumerate(opened_file):
                        sentence = sentence.replace('"', "'")
                        sentence = sentence.replace("'", '"')

                        # add sentence
                        if sentence not in self.cached_sentences:
                            self.db.insert({"title": sentence}, Sentences)
                            sentence_id = self.get_id(sentence, Sentences)
                            self.cached_sentences[sentence] = sentence_id
                        else:
                            sentence_id = self.cached_sentences[sentence]

                        # add link to file
                        item = {
                            "sentence_id": sentence_id,
                            "file_id": file_id,
                            "position": sentence_count,
                        }
                        self.db.insert(item, SentencesInFiles)

                        # create same structure for each sentence
                        for word_count, word in enumerate(sentence.split(" ")):
                            if word not in self.cached_words:
                                self.db.insert({"title": word}, Words)
                                word_id = self.get_id(word, Words)
                                self.cached_words[word] = word_id
                            else:
                                word_id = self.cached_words[word]
                            temp = {
                                "sentence_id": sentence_id,
                                "word_id": word_id,
                                "position": word_count,
                            }
                            self.db.insert(temp, WordsInSentences)

        self.db.close()

    def get_id(self, title: str, model: Base) -> int:
        q = """
            SELECT id from {model_table} where title='{title}' limit 1
            """
        for r in self.db.session.execute(q.format(title=title, model_table=model.__tablename__)):
            return r[0]
        return 0
