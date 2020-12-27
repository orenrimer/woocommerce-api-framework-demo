import random
from test_wooco.src.utilities.dbUtils import DbUtils


class CustomerDao(object):

    def __init__(self):
        self.db = DbUtils()

    def get_customer_by_email(self, email):
        sql = f"SELECT * FROM local.wp_users WHERE user_email = '{email}';"
        response = self.db.select(sql)
        return response

    def get_random_customer(self, qty=1):
        sql = f"SELECT * FROM local.wp_users ORDER BY ID DESC LIMIT 5000;"
        response = self.db.select(sql)
        return random.sample(response, k=int(qty))