import random

from test_wooco.src.utilities.dbUtils import DbUtils


class ProductsDao:

    def __init__(self):
        self.db = DbUtils()

    def select_product_by_name(self, name):
        sql = f"SELECT * FROM local.wp_posts WHERE post_title='{name}' and post_type='product';"
        product = self.db.select(sql)
        return product

    def select_product_by_id(self, product_id):
        sql = f"SELECT * FROM local.wp_posts WHERE ID='{product_id}' and post_type='product';"
        product = self.db.select(sql)
        return product

    def select_product_after_given_date(self, date):
        sql = f"SELECT * FROM local.wp_posts WHERE post_date > '{date}' and post_type='product' LIMIT 10000;"
        product = self.db.select(sql)
        return product

    def select_random_product_from_db(self, qty=1):
        sql = "SELECT * FROM local.wp_posts WHERE post_type='product' LIMIT 5000;"
        products = self.db.select(sql)
        return random.sample(products, k=qty)