from test_wooco.src.utilities.dbUtils import DbUtils


class OrdersDao:

    def __init__(self):
        self.db = DbUtils()

    def select_order_by_order_id(self, order_id):
        sql = f"SELECT * FROM local.wp_woocommerce_order_items WHERE order_id={order_id};"
        return self.db.select(sql)

    def select_order_details_by_order_item_id(self, order_item_id):
        sql = F"SELECT * FROM local.wp_woocommerce_order_itemmeta WHERE order_item_id={order_item_id};"
        response_db = self.db.select(sql)

        response_db_dict = {}
        for i in response_db:
            response_db_dict[i['meta_key']] = i['meta_value']

        return response_db_dict


    def select_order_status_by_order_id(self, order_id):
        sql = f"SELECT * FROM local.wp_wc_order_stats WHERE order_id={order_id};"
        return self.db.select(sql)


    def select_all_orders(self):
        sql = f"SELECT * FROM local.wp_wc_order_stats;"
        return self.db.select(sql)