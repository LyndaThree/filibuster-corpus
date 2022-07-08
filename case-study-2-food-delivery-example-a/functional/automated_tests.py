#!/usr/bin/env python

import requests
import os
import sys
import json

examples_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
sys.path.append(examples_path)

import helper

helper = helper.Helper("case-study-2-food-delivery-example-a")


def create_delivery_order():
    order_amount = 11.89
    response = requests.post(
        "{}/orders".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_amount": order_amount},
    )
    return response


def delete_delivery_order():
    order_amount = 15.89
    response = requests.delete(
        "{}/orders/10".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_id": 10, "order_amount": order_amount},
    )
    return response


def update_delivery_order():
    order_amount = 15.89
    response = requests.put(
        "{}/orders/10".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_id": 10, "order_amount": order_amount},
    )
    return response


def create_takeout_order():
    order_amount = 13.78
    response = requests.post(
        "{}/orders/takeout".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_amount": order_amount},
    )
    return response


def delete_takeout_order():
    order_amount = 13.78
    response = requests.delete(
        "{}/orders/takeout/10".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_id": 11, "order_amount": order_amount},
    )
    return response


def update_takeout_order():
    order_amount = 18.89
    response = requests.put(
        "{}/orders/takeout/10".format(helper.get_service_url("orders")),
        timeout=helper.get_timeout("orders"),
        json={"order_id": 11, "order_amount": order_amount},
    )
    return response


if __name__ == "__main__":

    # If 'DELETE_FAULT' environment variable is set, authorization is refused for deleting all takeout orders.
    # Note that 'DELETE_FAULT must be set for both the Takeout Auth service and this test file.
    if os.environ.get("DELETE_FAULT"):

        # these assertions will be true, becuase authorization is being granted for everything except deleting takout orders
        create_delivery_response = create_delivery_order()
        assert create_delivery_response.status_code == 201

        update_delivery_response = update_delivery_order()
        assert update_delivery_response.status_code == 200

        delete_delivery_response = delete_delivery_order()
        assert delete_delivery_response.status_code == 200

        create_takeout_response = create_takeout_order()
        assert create_takeout_response.status_code == 201

        update_takeout_response = update_takeout_order()
        assert update_takeout_response.status_code == 200

        # five repeated failures to authorize deleting a takeout order will trip the corresponding circuit breaker.
        # As a result of this, on the six attempt to delete a takeout order, we will see the status code change from 500 to 503,
        # since the circuit breaker is now open and rendering the Takeout Auth service unavailable.
        for i in range(6):
            delete_takeout_response = delete_takeout_order()
            try:
                assert delete_takeout_response.status_code == 200
            except AssertionError as e:
                print(
                    "Assertion error for delete authorization: status code",
                    delete_takeout_response.status_code,
                )

        # Since the cirucit breakers for the Orders service have proper placement,
        # authorization will still be granted for all other order operations, except deleting takeout
        create_delivery_response = create_delivery_order()
        assert create_delivery_response.status_code == 201

        update_delivery_response = update_delivery_order()
        assert update_delivery_response.status_code == 200

        delete_delivery_response = delete_delivery_order()
        assert delete_delivery_response.status_code == 200

        create_takeout_response = create_takeout_order()
        assert create_takeout_response.status_code == 201

        update_takeout_response = update_takeout_order()
        assert update_takeout_response.status_code == 200

    # If 'DELETE_FAULT' is not set, everything functions as intended, and authorization is granted for all order operations
    else:

        # these assertions will all be true
        create_delivery_response = create_delivery_order()
        assert create_delivery_response.status_code == 201

        update_delivery_response = update_delivery_order()
        assert update_delivery_response.status_code == 200

        delete_delivery_response = delete_delivery_order()
        assert delete_delivery_response.status_code == 200

        create_takeout_response = create_takeout_order()
        assert create_takeout_response.status_code == 201

        update_takeout_response = update_takeout_order()
        assert update_takeout_response.status_code == 200

        delete_takeout_response = delete_takeout_order()
        assert delete_takeout_response.status_code == 200
