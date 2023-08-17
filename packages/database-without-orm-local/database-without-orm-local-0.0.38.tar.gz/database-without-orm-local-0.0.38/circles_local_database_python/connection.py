import os
import sys
import mysql.connector
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import logger_local
from dotenv import load_dotenv
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)
from circles_local_database_python.cursor import Cursor

class Connection:
    DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
    COMPONENT_NAME = 'circles_local_database_python/connection.py'

    def __init__(self, database, host=None, user=None, password=None):
        logger_code_init = {
            'component_id': self.DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID,
            'component_name': self.COMPONENT_NAME,
            'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
            'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
            'developer_email': 'valeria.e@circ.zone and idan.a@circ.zone'
        }
        logger_local.init(object=logger_code_init)

        if not all([os.getenv("RDS_HOSTNAME"), os.getenv("RDS_USERNAME"), os.getenv("RDS_PASSWORD")]):
            logger_local.error(
                "Error: Add RDS_HOSTNAME, RDS_USERNAME and RDS_PASSWORD to .env")
            raise Exception("Environment variables not set.")

        self.host = host or os.getenv("RDS_HOSTNAME")
        self.database = os.getenv("RDS_DATABASE") or database
        self.user = user or os.getenv("RDS_USERNAME")
        self.password = password or os.getenv("RDS_PASSWORD")

        # Checking RDS_HOSTNAME suffix
        if not (self.host.endswith("circ.zone") or self.host.endswith("circlez.ai")):
            logger_local.error(
                f"Warning: Your RDS_HOSTNAME={self.host} which is not what is expected")

        self.connection = None
        self._cursor = None

        logger_local.end()

    def connect(self):
        logger_local.start("connect Attempting to connect...")
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.connection.can_consume_results
            self._cursor = self.connection.cursor()
            logger_local.info("connect Connected successfully!")
        except mysql.connector.Error as err:
            logger_local.exception(object=err)
            raise
        logger_local.end()
        return self

    def close(self):
        logger_local.start()
        try:
            if self.cursor:
                self.cursor.close()
                logger_local.info("Cursor closed successfully.")
        except Exception as e:
            logger_local.exception(object=e)

        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                logger_local.info("Connection closed successfully.")
        except Exception as e:
            logger_local.exception("connection.py close()", object=e)
        logger_local.end()

    def cursor(self, sql_parameters=None):
        logger_local.start("cursor asked", object={
                           "sql_parameters": sql_parameters})
        cursor_instance = Cursor(self.connection.cursor(sql_parameters))
        logger_local.end(object={'cursor': "Cursor created successfully"})
        return cursor_instance

    def commit(self):
        logger_local.start("commiting to data base")
        self.connection.commit()
        logger_local.end(object={})

    def set_schema(self, new_database):
        logger_local.start()
        self.database = new_database
        if self.connection and self.connection.is_connected():
            try:
                self.cursor.execute(f"USE {new_database};")
                logger_local.info(f"Switched to database: {new_database}")
            except mysql.connector.Error as err:
                logger_local.exception(object=err)
                raise
        else:
            logger_local.exception(
                "Connection is not established. The database will be used on the next connect.")
        logger_local.end()
