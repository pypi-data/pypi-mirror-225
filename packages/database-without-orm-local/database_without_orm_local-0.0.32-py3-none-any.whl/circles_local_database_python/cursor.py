import os
import sys
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'circles_local_database_python')
sys.path.append(src_path)

from logger_local.LoggerLocal import logger_local

load_dotenv()

class Cursor():
    DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13

    def __init__(self,cursor) -> None:
        self.cursor=cursor
        logger_local.init(object={'component_id': self.DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID})
    
    def execute(self,query,params=None):
        params_str=""
        for param in params:
            params_str+=str(param)
        logger_local.start(object={"query":query,"params":params})
        self.cursor.execute(query,params)
        logger_local.end()

    def fetchall(self):
        logger_local.start()
        result=self.cursor.fetchall()
        logger_local.end()
        return result

    def fetchone(self):
        logger_local.start()
        result=self.cursor.fetchone()
        logger_local.end()
        return result

    def description(self):
        logger_local.start()
        result=self.cursor.description
        logger_local.end()
        return result

    def lastrowid(self):
        logger_local.start()
        result=self.cursor.lastrowid
        logger_local.end()
        return result
    
    def close(self):
        logger_local.start()
        self.cursor.close()
        logger_local.end()