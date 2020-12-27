import json
import os
from test_wooco.src.dao.orders_dao import OrdersDao
from test_wooco.src.utilities.woocoApiUtils import WoocoApiUtils


class OrdersHelper(object):

    def __init__(self):
        self.wcapi = WoocoApiUtils()
        self.file_dir = os.path.dirname(os.path.realpath(__file__))

    def get_order_by_id(self, order_id, expected_status_code=200):
        return self.wcapi.get(endpoint=f"orders/{order_id}", expected_status_code=expected_status_code)

    def get_all_orders(self):
        all_products = []
        max_pages = 1000
        page_num = 1
        while page_num < max_pages:
            param = {'per_page': 100, 'page': page_num}
            response = self.wcapi.get(wc_endpoint='products', params=param)
            if response:
                page_num += 1
                all_products.extend(response)
            else:
                print("No results on page number {}. End loop of calling products.".format(page_num))
                break

        return all_products

    def create_order(self, additional_args=None, expected_status_code=201):
        payload_template = os.path.join(self.file_dir, "..", 'templates', 'create_order_payload.json')

        with open(payload_template) as f:
            payload = json.load(f)

        if additional_args:
            assert isinstance(additional_args, dict), f"'additional_args' must be dict, fount{type(additional_args)}"
            payload.update(additional_args)
        return self.wcapi.post(endpoint='orders', data=payload, expected_status_code=expected_status_code)


    def update_order(self, order_id, payload=None, expected_status_code=200):
        if payload:
            assert isinstance(payload, dict), f"'additional_args' must be dict, fount{type(payload)}"
        return self.wcapi.put(endpoint=f'orders/{order_id}', data=payload, expected_status_code=expected_status_code)


    def validate_order_created(self, order_json, expected_products, expected_customer_id):
        # validate response
        assert order_json['customer_id'] == expected_customer_id, f"parameter 'customer_id' is invalid. " \
                                                                  f"expected {expected_customer_id}, " \
                                                                  f"got{order_json['customer_id']}"
        # check db
        order_id = order_json['id']
        orders_db = OrdersDao()
        line_info = orders_db.select_order_by_order_id(order_id)
        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']
        assert len(line_items) == len(expected_products), f"expected {expected_products} item in order, " \
                                                          f"got {len(order_json['line_items'])}"

        expected_products_ids = [i['product_id'] for i in order_json['line_items']]
        line_id_ids = [i['order_item_id'] for i in line_items]
        for item_id in line_id_ids:
            line_item_details = orders_db.select_order_details_by_order_item_id(item_id)
            line_item_id = line_item_details['_product_id']
            assert int(line_item_id) in expected_products_ids, f"missing item in line items. missing product id: {line_item_id} "
            assert str(line_item_details['_qty']) == str(order_json['line_items'][0]['quantity'])
