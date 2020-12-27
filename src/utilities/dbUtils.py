import logging as logger
import os
import pymysql.cursors
from test_wooco.src.config.hosts_config import DB_HOST
from test_wooco.src.utilities.credentialUtils import CredentialUtils


class DbUtils:
    def __init__(self):
        self.credentials = CredentialUtils.get_db_credentials()
        machine = os.environ.get('MACHINE')
        env = os.environ.get('ENV', 'test')
        wp_host = os.environ.get('WP_HOST')
        self.host = DB_HOST[machine][env]['host']
        self.port = DB_HOST[machine][env]['port']
        self.db = DB_HOST[machine][env]['database']


    def connect(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.credentials['user'],
                                     password=self.credentials['password'],
                                     db=self.db,
                                     port=self.port)
        return connection

    def select(self, sql):
        connection = self.connect()
        try:
            logger.debug(f'executing sql: {sql}')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            response = cursor.fetchall()
            cursor.close()
        except Exception as e:
            raise Exception(f"Failed running sql {sql} \n Error: {str(e)}")
        finally:
            connection.close()

        return response
