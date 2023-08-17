from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import Dict

import mysql.connector
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBProvider(metaclass=ABCMeta):
    def __init__(self, db_config: Dict):
        self._connection = self._connect_(db_config)
        self._db_config = db_config

    @staticmethod
    @abstractmethod
    def _connect_(db_config: Dict):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def create_db(self, name: str):
        pass

    @abstractmethod
    def drop_db(self, name: str):
        pass

    @abstractmethod
    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        pass

    @abstractmethod
    def drop_table(self, name: str, db_name: str = None):
        pass

    @abstractmethod
    def select(self):
        pass


class MYSQLProvider(DBProvider):
    def _execute_(self, query: str):
        try:
            cursor = self._connection.cursor()
        except mysql.connector.errors.OperationalError as e:
            self._connection = self._connect_(self._db_config)
            cursor = self._connection.cursor()

        cursor.execute(query)
        return cursor

    @staticmethod
    def _connect_(db_config: Dict):
        return mysql.connector.connect(**db_config)

    def close(self):
        self._connection.close()

    def create_db(self, name: str):
        query = f"""
            CREATE DATABASE IF NOT EXISTS {name}
        """

        self._execute_(query)

    def drop_db(self, name: str):
        query = f"""
            DROP DATABASE IF EXISTS {name}
        """

        self._execute_(query)

    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        fields_str = ',\n'.join([f'{name} {field_type}' for name, field_type in fields.items()])

        query = f"""
            {f'USE {db_name};' if db_name else ''}
            CREATE {'TEMPORARY ' if temporary else ''}TABLE IF NOT EXISTS {name} (
                {fields_str}
            ) ENGINE = InnoDB;
        """

        self._execute_(query)

    def drop_table(self, name: str, db_name: str = None):
        query = f"""
            {f'USE {db_name};' if db_name else ''}
            DROP TABLE IF EXISTS {name};
        """

        self._execute_(query)

    def select(self):
        pass


class PostgresProvider(DBProvider):
    def _execute_(self, query: str, db_name: str = None, isolation_level: int = None):
        if db_name:
            self._connection.close()
            self._db_config['database'] = db_name

            self._connection = self._connect_(self._db_config)

        if isolation_level is not None:
            self._connection.set_isolation_level(isolation_level)

        cursor = self._connection.cursor()
        cursor.execute(query)
        self._connection.commit()
        return cursor

    @staticmethod
    def _connect_(db_config: Dict):
        return psycopg2.connect(**db_config)

    def close(self):
        self._connection.close()

    def create_db(self, name: str):
        query = f"""
            CREATE DATABASE {name};
        """

        try:
            self._execute_(query, isolation_level=ISOLATION_LEVEL_AUTOCOMMIT)
        except psycopg2.Error as e:
            if e.pgcode != '42P04':  # DB exists
                raise e

    def drop_db(self, name: str):
        query = f"""
            DROP DATABASE {name}; 
        """

        try:
            self._execute_(query, isolation_level=ISOLATION_LEVEL_AUTOCOMMIT, db_name='postgres')
        except psycopg2.Error as e:
            if e.pgcode != '42P04':  # DB does not exist
                raise e

    def create_table(self, name: str, fields: Dict, db_name: str = None, temporary: bool = False):
        fields_str = ',\n'.join([f'{name} {field_type}' for name, field_type in fields.items()])

        query = f"""
            CREATE {'TEMPORARY ' if temporary else ''}TABLE IF NOT EXISTS {name} (
                {fields_str}
            )
        """

        self._execute_(query, db_name=db_name)

    def drop_table(self, name: str, db_name: str = None):
        query = f"""
            DROP TABLE IF EXISTS {name};
        """

        self._execute_(query)

    def select(self):
        pass


class DBTypes(Enum):
    MYSQL = MYSQLProvider
    PostgresSQL = PostgresProvider


db = DBTypes.MYSQL.value(dict(host='3.79.32.214',
                              user='hide',
                              password='Neh,byf2009'))

db.create_db('task5')

db.create_table('log_data',
                dict(id='INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
                     row_num='INT NOT NULL',
                     selection='VARCHAR(500)',
                     aggregate='VARCHAR(500)'),
                db_name='task5')

db.drop_table('log_data', db_name='task5')

db.drop_db('task5')

db.close()

# -----------------------------------------------

db = DBTypes.PostgresSQL.value(dict(host='3.79.32.214',
                                    user='hide',
                                    password='Neh,byf2009',
                                    database='postgres'))

db.create_db('task5')

db.create_table('log_data',
                dict(id='SERIAL PRIMARY KEY',
                     row_num='INT NOT NULL',
                     selection='VARCHAR(500)',
                     aggregate='VARCHAR(500)'),
                temporary=True,
                db_name='task5'
                )

db.drop_table('log_data')

db.drop_db('task5')

db.close()




# create_table = """
#     CREATE TEMPORARY TABLE customers (
#         id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#         row_num INT NOT NULL,
#         selection VARCHAR(255),
#         aggregate VARCHAR(255)
#     ) ENGINE = InnoDB;
# """


#
# # Task 1: Gather statistics by IP addresses and browsers
# query = """
#     SELECT
#         SUBSTRING_INDEX(SUBSTRING_INDEX(ip, ',', 1), ' ', -1) AS ip_address,
#         SUBSTRING_INDEX(user_agent, ' ', 1) AS browser,
#         COUNT(*) AS request_count
#     FROM
#         log_data
#     GROUP BY
#         ip_address, browser
#     ORDER BY
#         request_count DESC
#     LIMIT 10
# """
#
# cursor.execute(query)
# results = cursor.fetchall()
#
# print("Top 10 IP addresses and browsers by request count:")
# for row in results:
#     ip_address, browser, request_count = row
#     print(f"IP: {ip_address}, Browser: {browser}, Request Count: {request_count}")
