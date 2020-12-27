import logging as logger
import pytest
from test_wooco.src.dao.products_dao import ProductsDao
from test_wooco.src.helpers.product_helper import ProductHelper
from test_wooco.src.utilities.genericUtils import generate_random_string


pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid26
def test_create_product_only_name():
    logger.info("TEST::create a new product with name only")
    name = generate_random_string()

    # create a new product
    product_helper = ProductHelper()
    product_json = product_helper.create_product(name)
    assert product_json['name'] == name, f"expected name: {name}, got {product_json['name']}"

    # get product from db
    new_product_id = product_json['id']
    products_db = ProductsDao()
    product_db = products_db.select_product_by_id(new_product_id)

    # verify product json corresponds to product in db
    assert product_db[0]['post_title'] == name, f"expected name: {name}, got {product_db[0]['post_title']}"