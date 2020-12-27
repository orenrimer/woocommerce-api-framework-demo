import logging as logger
import pytest
from test_wooco.src.dao.orders_dao import OrdersDao
from test_wooco.src.dao.products_dao import ProductsDao
from test_wooco.src.helpers.customer_helper import CustomerHelper
from test_wooco.src.helpers.orders_helper import OrdersHelper



pytestmark = [pytest.mark.orders, pytest.mark.smoke]

class TestCreateOrdersSmoke:

    @pytest.fixture(scope="session")
    def helpers(self):
        products_db = ProductsDao()
        orders_db = OrdersDao()
        orders_helper = OrdersHelper()
        customer_helper = CustomerHelper()
        random_products = products_db.select_random_product_from_db()
        yield {'products_db': products_db,
               'orders_db': orders_db,
               'orders_helper': orders_helper,
               'customer_helper': customer_helper,
               'random_product': random_products
               }

    @pytest.mark.tcid48
    def test_create_order_as_guest(self, helpers):
        logger.info("TEST::create an order with a guest account")

        # get a random product from db
        random_products = helpers['random_product']

        order_info = {"line_items": []}

        for random_product in random_products:
            if random_product['ID'] not in order_info['line_items']:
                order_info['line_items'].append({'product_id':random_product['ID'],
                                                 'quantity': 1})

        # make the call
        orders_helper = helpers['orders_helper']
        order_json = orders_helper.create_order(additional_args=order_info)
        orders_helper.validate_order_created(order_json, random_products, 0)


    @pytest.mark.tcid49
    def test_create_order_with_new_user(self, helpers):
        logger.info("TEST::create an order with a new user account")

        # create a new customer
        customer_helper = helpers['customer_helper']
        new_customer_json = customer_helper.create_customer()
        new_customer_id = new_customer_json['id']
        assert new_customer_json, "response create customer is empty"


        random_products = helpers['random_product']
        order_info = {"line_items": [],
                      'customer_id': new_customer_id}

        for random_product in random_products:
            order_info['line_items'].append({'product_id':random_product['ID'],
                                            'quantity': 1})

        orders_helper = helpers['orders_helper']
        order_json = orders_helper.create_order(additional_args=order_info)
        orders_helper.validate_order_created(order_json, random_products, new_customer_id)