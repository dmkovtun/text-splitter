import sqlalchemy
import logging
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import IntegrityError, OperationalError
from helpers.mysql_connection_string import mysql_connection_string


class Connection(object):
    """Database connection class"""

    def __init__(self, *args, **kwargs):
        """Init method, needs DB_URL inside kwargs for correct work"""
        self._db_address = None

        self.session = None
        self._engine = None
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        try:
            self._db_address = mysql_connection_string()
        except KeyError as ke:
            self.logger.error(ke)

        if not self.connect():
            self.logger.critical("DB_URL: {}".format(self._db_address))
            raise Exception("Database is disconnected")

    def connect(self) -> bool:
        """Connects to database

        Returns:
            True if connected correctly
        """
        try:
            self._engine = create_engine(self._db_address, encoding="UTF-8")
            session = sessionmaker(bind=self._engine, autocommit=True)
            self.session = session()

            # will raise exception if cannot select
            self.session.execute("SELECT 1")
        except sqlalchemy.exc.OperationalError as oe:
            self.logger.error("Engine is not created {}".format(oe))
            return False
        return True

    def close(self) -> None:
        """Closes current session"""
        self.session.close()

    def insert(self, item, model):
        """Inserts item to db model

        :param item: item to be inserted
        :param model: table model to insert item to
        """
        insert_stmt = mysql.insert(model).values(**item)
        upd_stmt = insert_stmt.on_duplicate_key_update(**item)
        try:
            self.session.execute(upd_stmt)
        except OperationalError as op:
            self.logger.error(f"Insert failed: {op}")
        except IntegrityError as ie:
            self.logger.error(f"Insert failed: {ie}")

    def update(self, item, model):
        """Updates item in db model

        :param item: item to be updated
        :param model: table model to update item to
        """
        upd_stmt = update(model).values(**item).where(model.id == item["id"])
        try:
            self.session.execute(upd_stmt)
        except OperationalError as op:
            self.logger.error("Update failed: {}".format(op))
