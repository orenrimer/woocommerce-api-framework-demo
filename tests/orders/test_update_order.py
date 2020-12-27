import pytest
from test_wooco.src.dao.orders_dao import OrdersDao
from test_wooco.src.helpers.orders_helper import OrdersHelper
from test_wooco.src.utilities.genericUtils import generate_random_string


pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.fixture(scope='module')
def helpers_setup():
    orders_helper = OrdersHelper()
    orders_db = OrdersDao()
    helpers = {'orders_helper': orders_helper, 'orders_db': orders_db}
    return helpers


@pytest.mark.parametrize("new_status",
                         [pytest.param('pending', marks=pytest.mark.tcid52),
                          pytest.param('failed', marks=pytest.mark.tcid53),
                          pytest.param('cancelled', marks=pytest.mark.tcid54),
                          pytest.param('refunded', marks=pytest.mark.tcid55),
                          pytest.param('completed', marks=pytest.mark.tcid56),
                          pytest.param('on-hold', marks=pytest.mark.tcid57),
                          ])
def test_update_order_status(helpers_setup, new_status):
    # create new order
    orders_helper = helpers_setup['orders_helper']
    order_json = orders_helper.create_order()
    order_id = order_json['id']
    new_status = new_status

    # get the curr order status
    curr_status = order_json['status']
    assert curr_status != new_status, f"invalid order status. new order status already equal to new status {new_status}"
    assert curr_status == 'processing', f"invalid order status for a new order. new order status expected to be processing, " \
                                        f"got {curr_status}"

    # update the status
    orders_helper.update_order(order_id=order_id, payload={'status': new_status})

    # retrieve the order info one more time
    order_info = orders_helper.get_order_by_id(order_id)

    # verify the order status in db
    assert order_info['status'] == new_status, f"failed to update order's status. expected to be {new_status}, " \
                                               f"got {order_info['status']}"


@pytest.mark.tcid58
def test_update_order_status_with_random_status(helpers_setup):
    # create new order
    orders_helper = helpers_setup['orders_helper']
    order_json = orders_helper.create_order()
    order_id = order_json['id']
    new_status = generate_random_string()

    # get the curr order status
    curr_status = order_json['status']
    assert curr_status != new_status, f"invalid order status. new order status already equal to new status {new_status}"
    assert curr_status == 'processing', f"invalid order status for a new order. new order status expected to be processing, " \
                                        f"got {curr_status}"

    # try to update the status
    response_json = orders_helper.update_order(order_id=order_id, payload={'status': new_status},
                                               expected_status_code=400)

    # assert error msg in response
    assert response_json['code'] == 'rest_invalid_param', f"invalid error code. " \
                                                          f"expected code: 'rest_invalid_param', got{response_json['code']}"
    assert response_json['message'] == 'Invalid parameter(s): status', f"invalid error message. " \
                                                                       f"expected message: 'Invalid parameter(s), got{response_json['message']}"



@pytest.mark.tcid59
def test_update_order_customer_note(helpers_setup):
    new_customer_note = generate_random_string(length=40)

    # create new order
    orders_helper = helpers_setup['orders_helper']
    order_json = orders_helper.create_order()
    order_id = order_json['id']

    # get curr customer note
    order_customer_note = order_json['customer_note']

    # update the customer note
    payload = {"customer_note":new_customer_note}
    orders_helper.update_order(order_id=order_id, payload=payload)

    # verify customer note
    updated_order_json = orders_helper.get_order_by_id(order_id)
    assert updated_order_json['customer_note'] == new_customer_note