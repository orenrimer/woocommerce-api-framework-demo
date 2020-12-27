from test_wooco.src.utilities.genericUtils import generate_random_email
from test_wooco.src.utilities.requestUtils import RequestUtils


class CustomerHelper(object):
    def __init__(self):
        self.requests = RequestUtils()

    def create_customer(self, email=None, password=None, expected_status_code=201, **kwargs):
        if not email:
            email = generate_random_email()
        if not password:
            password = "testpassword123"

        payload = {'email': email, 'password': password}
        payload.update(kwargs)

        customer_json = self.requests.post(endpoint='customers', payload=payload,
                                           expected_status_code=expected_status_code)
        return customer_json

    def get_customer(self, **kwargs):
        payload = dict()
        payload.update(kwargs)

        all_customers = []
        max_pages = 1000
        for i in range(1, max_pages + 1):
            if 'per_page' not in payload.keys():
                payload['per_page'] = 100

            payload['page'] = i
            response_json = self.requests.get(endpoint='customers', payload=payload)

            if not response_json: break
            else: all_customers.extend(response_json)
        else:
            raise Exception(f"can't find all products")

        return all_customers

    def get_customer_by_id(self, customer_id):
        return self.requests.get(endpoint=f'customers/{customer_id}')
