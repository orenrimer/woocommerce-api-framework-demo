import logging as logger
from datetime import datetime, timedelta
import pytest
from test_wooco.src.dao.products_dao import ProductsDao
from test_wooco.src.helpers.product_helper import ProductHelper


@pytest.mark.reggression
class TestGetProductWithFilter:

    @pytest.mark.tcid51
    def test_get_product_with_filter_after(self):
        logger.info("TEST::get all products created after a certain date")
        _after_date = datetime.now().replace(microsecond=0) - timedelta(days=30)
        after_date = _after_date.isoformat()

        product_helper = ProductHelper()
        products_json = product_helper.get_product(after=after_date)
        assert products_json, f"no products returned"

        products_db = ProductsDao()
        products_db_list = products_db.select_product_after_given_date(after_date)
        num_of_products = len(products_db_list)
        assert num_of_products == len(products_json), f"missing products. num of expected products: {num_of_products}," \
                                                      f"got {len(products_json)}"

        response_ids = [product['id'] for product in products_json]
        db_ids = [product['ID'] for product in products_db_list]
        diff = list(set(response_ids) - set(db_ids))
        assert not diff, f"API products id's doesn't match the id's from DB"