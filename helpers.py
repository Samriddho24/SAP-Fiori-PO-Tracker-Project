"""
helpers.py — Utility functions for ZFI_PO_TRACKER
KIIT Manufacturing Ltd. (KML)
Student: Samriddho Kar | Roll No: 23053296
"""

from datetime import date, datetime
from typing import Union


def compute_delay_bucket(delivery_date_str: str) -> dict:
    """
    Compute delay in days from today and assign a delay bucket.

    Buckets:
        On Time    : delay <= 15 days
        16-30 Days : 16 <= delay <= 30
        31-60 Days : 31 <= delay <= 60
        >60 Days   : delay > 60

    Args:
        delivery_date_str: ISO date string "YYYY-MM-DD"

    Returns:
        dict with keys: delay_days, delay_bucket, status_icon (Success/Warning/Error)
    """
    if not delivery_date_str:
        return {"delay_days": 0, "delay_bucket": "On Time", "status_icon": "Success"}

    try:
        delivery_date = datetime.strptime(delivery_date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"delay_days": 0, "delay_bucket": "On Time", "status_icon": "Success"}

    today = date.today()
    delay_days = (today - delivery_date).days

    if delay_days <= 15:
        bucket = "On Time"
        icon   = "Success"
    elif delay_days <= 30:
        bucket = "16-30 Days"
        icon   = "Warning"
    elif delay_days <= 60:
        bucket = "31-60 Days"
        icon   = "Error"
    else:
        bucket = ">60 Days"
        icon   = "Error"

    return {
        "delay_days":   delay_days,
        "delay_bucket": bucket,
        "status_icon":  icon,
    }


def calculate_total(quantity: Union[int, float], unit_price: Union[int, float]) -> float:
    """
    Calculate line item total.

    Args:
        quantity:   order quantity
        unit_price: price per unit in INR

    Returns:
        float — net line value
    """
    return round(float(quantity) * float(unit_price), 2)


def apply_discount(net_value: float, discount_pct: float) -> dict:
    """
    Apply a percentage discount to a net value.

    Args:
        net_value:    original amount in INR
        discount_pct: discount percentage (e.g. 5.0 for 5%)

    Returns:
        dict with keys: original, discount_amount, final_value
    """
    discount_amount = round(net_value * (discount_pct / 100), 2)
    final_value     = round(net_value - discount_amount, 2)
    return {
        "original":        net_value,
        "discount_pct":    discount_pct,
        "discount_amount": discount_amount,
        "final_value":     final_value,
    }


def get_status_color(delay_bucket: str) -> str:
    """
    Map delay bucket to SAP Fiori semantic colour token.

    Returns: 'Success' | 'Warning' | 'Error'
    """
    mapping = {
        "On Time":    "Success",
        "16-30 Days": "Warning",
        "31-60 Days": "Error",
        ">60 Days":   "Error",
    }
    return mapping.get(delay_bucket, "None")


def format_inr(amount: float) -> str:
    """Format a float as Indian Rupee string e.g. ₹ 2,45,000.00"""
    s = f"{amount:,.2f}"
    return f"₹ {s}"
