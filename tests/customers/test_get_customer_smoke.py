import logging as logger
import pytest
from test_wooco.src.helpers.customer_helper import CustomerHelper


pytestmark = [pytest.mark.customers, pytest.mark.smoke]

@pytest.mark.tcid30
def test_get_all_customers():
    logger.info("TEST::get all customers")
    customer_helper = CustomerHelper()
    customers = customer_helper.get_customer()
    assert customers, f"customers list is empty"