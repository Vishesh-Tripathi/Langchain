import json
from pathlib import Path
from langchain_core.tools import tool


DATA_FILE = Path(__file__).resolve().parent / "data.json"


def load_data() -> dict:
    """Load SmartKart data from the JSON file."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@tool
def get_order_status(order_id: str) -> str:
    """Get the current status of a SmartKart order using its order ID."""

    data = load_data()

    order = data["order_database"].get(order_id)

    if order:
        return order["status"]

    return "Order not found"


@tool
def delivery_charge_calculator(
    order_value: float,
    customer_type: str
) -> float:
    """
    Calculate the delivery charge based on the order value
    and customer type.
    """

    data = load_data()

    rules = data["delivery_charge_rules"]

    if customer_type not in rules:
        return -1

    customer_rule = rules[customer_type]

    if customer_type == "Premium":
        return customer_rule["delivery_charge"]

    minimum_amount = customer_rule[
        "minimum_free_delivery_amount"
    ]

    if order_value >= minimum_amount:
        return customer_rule[
            "delivery_charge_above_minimum"
        ]

    return customer_rule[
        "delivery_charge_below_minimum"
    ]


@tool
def estimate_delivery_time(shipping_type: str) -> str:
    """
    Get the estimated delivery time based on the shipping type.
    """

    data = load_data()

    return data["shipping_options"].get(
        shipping_type,
        "Invalid shipping type"
    )