import sqlite3
from loguru import logger


class DatabaseHandler:
    """Handler for work with SQL queries"""

    def __new__(cls, *args, **kwargs):
        """Singleton pattern realisation"""
        logger.debug("Creating/getting of a database handler object.")
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)
        logger.debug("Creating/getting of a database handler object - Success.")
        return cls.instance

    def __init__(self, app):
        """Initialisation of a db handler object"""
        logger.debug("Initialisation of a database handler.")
        self.__app = app
        self.__connection = sqlite3.connect(self.__app.config['DATABASE'])
        self.__connection.row_factory = sqlite3.Row
        logger.debug("Initialisation of a database handler - Success.")

    def create_start_table(self):
        """Create the test table in the DB"""
        logger.debug("Create of a test table.")
        with self.__app.open_resource('start.sql', mode='r') as f:
            self.__connection.cursor().executescript(f.read())
        self.__connection.commit()
        self.__connection.close()
        logger.debug("Create of a test table - Success.")

    def insert_record(self, date, temperature):
        """Insertion of data into records table"""
        logger.debug("Insertion of a records.")
        query = f'''INSERT INTO records (date, temperature) VALUES ('{date}', {temperature})'''
        try:
            logger.debug("Load query and execute.")
            self.__connection.cursor().execute(query)
            self.__connection.commit()
            logger.debug("Execute query - Success.")
        except sqlite3.Error as err:
            logger.error("There are a troubles with the db ¯\_(ツ)_/¯:", err)
