from test_wooco.src.utilities.genericUtils import generate_random_string
from test_wooco.src.utilities.requestUtils import RequestUtils


class ProductHelper(object):

    def __init__(self):
        self.requests = RequestUtils()

    def create_product(self, name=None, **kwargs):
        if not name: name = generate_random_string(prefix='product')
        payload = {"name":name}
        payload.update(kwargs)
        product_json = self.requests.post(endpoint='products', payload=payload)
        return product_json

    def get_product_by_id(self, product_id):
        product_json = self.requests.get(endpoint=f"products/{product_id}")
        return product_json

    def get_product(self, **kwargs):
        payload = dict()
        payload.update(kwargs)
        all_products = []
        max_pages = 1000
        for i in range(1, max_pages+1):
            if 'per_page' not in payload.keys():
                payload["per_page"] = 100

            payload['page'] = i
            products_json = self.requests.get(endpoint='products', payload=payload)

            if not products_json: break
            else: all_products.extend(products_json)
        else:
            raise Exception(f"can't find all products")
        return all_products