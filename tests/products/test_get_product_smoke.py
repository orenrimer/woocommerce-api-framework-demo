import pytest
from test_wooco.src.dao.products_dao import ProductsDao
from test_wooco.src.helpers.product_helper import ProductHelper



pytestmark = [pytest.mark.products, pytest.mark.smoke]


class TestGetProductSmoke:

    @classmethod
    def setup(cls):
        cls.product_helper = ProductHelper()
        cls.products_dao = ProductsDao()

    @pytest.mark.tcid24
    def test_get_all_products(self):
        response = self.product_helper.get_product()
        assert response, "product list is empty"


    @pytest.mark.tcid25
    def test_get_product_by_id(self):
        # get random product from db
        random_product = self.products_dao.select_random_product_from_db()[0]
        product_id = random_product['ID']

        # get API response
        response = self.product_helper.get_product_by_id(product_id)

        # verify product in response corresponds to db
        assert response['id'] == product_id, f"expected product id: {product_id}, got {response['id']}"
        assert response['name'] == random_product['post_title'], f"expected product name: {random_product['post_title']}, " \
                                                                 f"got {response['name']}"