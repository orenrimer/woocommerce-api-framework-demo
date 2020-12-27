import logging as logger
import pytest
from test_wooco.src.dao.orders_dao import OrdersDao
from test_wooco.src.helpers.orders_helper import OrdersHelper


pytestmark = [pytest.mark.order, pytest.mark.smoke]

@pytest.mark.tcid31
def test_get_all_orders():
    logger.info("TEST::get all orders")
    orders_helper = OrdersHelper()
    orders_list = orders_helper.get_all_orders()

    orders_db = OrdersDao()
    db_orders_list = orders_db.select_all_orders()
    assert len(orders_list) == len(db_orders_list), f"missing orders"