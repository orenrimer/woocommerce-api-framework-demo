import logging as logger
import pytest
from test_wooco.src.dao.customer_dao import CustomerDao
from test_wooco.src.helpers.customer_helper import CustomerHelper
from test_wooco.src.utilities.genericUtils import generate_random_email_and_password


pytestmark = [pytest.mark.customers, pytest.mark.smoke]


class TestCreateCustomerSmoke:

    @pytest.fixture()
    def setup(self):
        self.customer_helper = CustomerHelper()
        self.customers_db = CustomerDao()

    @pytest.mark.tcid29
    def test_create_customer_only_email_and_password(self, setup):
        logger.info("TEST::create a new customer with only email and password")

        # create random customer info
        ep = generate_random_email_and_password()
        email = ep['email']
        password = ep['password']

        # make the call
        customer_info = self.customer_helper.create_customer(email=email, password=password)

        # verify API response info
        assert customer_info['email'] == email, f"expected email: {email}, got {customer_info['email']}"
        assert customer_info['first_name'] == "", "customer first name should be empty"

        # verify customer created in DB
        customer_db = self.customers_db.get_customer_by_email(customer_info['email'])
        assert customer_db[0]['ID'] == customer_info['id'], f"expected id: {customer_info['id']}, got {customer_db[0]['id']}"


    @pytest.mark.tcid47
    def test_create_customer_with_existing_email_fails(self, setup):
        logger.info("TEST::create a new customer with an existing email")
        customer_db = self.customers_db.get_random_customer()
        email = customer_db[0]['user_email']
        response = self.customer_helper.create_customer(email=email, expected_status_code=400)
        assert response['code'] == "registration-error-email-exists", f"excepted response code: " \
                                                                      f"registration-error-email-exists, " \
                                                                      f"got {response['code']}"