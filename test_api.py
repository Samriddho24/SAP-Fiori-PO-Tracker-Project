"""
test_api.py — API Test Suite for ZFI_PO_TRACKER
Uses pytest + requests. Refactored to use BASE_URL constant.
Student: Samriddho Kar | Roll No: 23053296
"""

import pytest
import requests

BASE_URL = "http://localhost:8000"


# ── Health ────────────────────────────────────────────────────────────────────
class TestHealth:
    def test_root_returns_200(self):
        resp = requests.get(f"{BASE_URL}/")
        assert resp.status_code == 200

    def test_root_returns_app_name(self):
        resp = requests.get(f"{BASE_URL}/")
        data = resp.json()
        assert data["app"] == "ZFI_PO_TRACKER"

    def test_root_returns_company(self):
        resp = requests.get(f"{BASE_URL}/")
        data = resp.json()
        assert "KML" in data["company"]


# ── Purchase Orders ───────────────────────────────────────────────────────────
class TestPurchaseOrders:
    def test_list_pos_returns_200(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders")
        assert resp.status_code == 200

    def test_list_pos_has_total_field(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders")
        data = resp.json()
        assert "total" in data
        assert data["total"] >= 0

    def test_list_pos_has_purchase_orders_list(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders")
        data = resp.json()
        assert "purchase_orders" in data
        assert isinstance(data["purchase_orders"], list)

    def test_each_po_has_delay_bucket(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders")
        data = resp.json()
        for po in data["purchase_orders"]:
            assert "delay_bucket" in po
            assert po["delay_bucket"] in ["On Time", "16-30 Days", "31-60 Days", ">60 Days"]

    def test_each_po_has_status_icon(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders")
        data = resp.json()
        for po in data["purchase_orders"]:
            assert "status_icon" in po
            assert po["status_icon"] in ["Success", "Warning", "Error"]

    def test_filter_by_plant_kp01(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders?plant=KP01")
        data = resp.json()
        for po in data["purchase_orders"]:
            assert po["plant"] == "KP01"

    def test_filter_by_plant_kp02(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders?plant=KP02")
        data = resp.json()
        for po in data["purchase_orders"]:
            assert po["plant"] == "KP02"

    def test_get_single_po(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/4500021873")
        assert resp.status_code == 200
        data = resp.json()
        assert data["po_number"] == "4500021873"

    def test_get_nonexistent_po_returns_404(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/9999999999")
        assert resp.status_code == 404

    def test_single_po_has_items(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/4500021875")
        data = resp.json()
        assert "items" in data
        assert len(data["items"]) > 0

    def test_single_po_items_have_line_total(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/4500021875")
        data = resp.json()
        for item in data["items"]:
            assert "line_total" in item
            assert item["line_total"] > 0


# ── Delay Summary (KPI) ───────────────────────────────────────────────────────
class TestDelaySummary:
    def test_delay_summary_returns_200(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/delay-summary")
        assert resp.status_code == 200

    def test_delay_summary_has_all_buckets(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/delay-summary")
        data = resp.json()
        assert "On Time"    in data
        assert "16-30 Days" in data
        assert "31-60 Days" in data
        assert ">60 Days"   in data
        assert "total"      in data

    def test_delay_summary_counts_sum_to_total(self):
        resp = requests.get(f"{BASE_URL}/purchase-orders/delay-summary")
        data = resp.json()
        bucket_sum = (
            data["On Time"] + data["16-30 Days"] +
            data["31-60 Days"] + data[">60 Days"]
        )
        assert bucket_sum == data["total"]


# ── Master Data ───────────────────────────────────────────────────────────────
class TestMasterData:
    def test_vendors_returns_200(self):
        resp = requests.get(f"{BASE_URL}/vendors")
        assert resp.status_code == 200

    def test_vendors_list_not_empty(self):
        resp = requests.get(f"{BASE_URL}/vendors")
        data = resp.json()
        assert data["total"] > 0

    def test_plants_returns_200(self):
        resp = requests.get(f"{BASE_URL}/plants")
        assert resp.status_code == 200

    def test_plants_has_three_kml_plants(self):
        resp = requests.get(f"{BASE_URL}/plants")
        data = resp.json()
        codes = [p["plant_code"] for p in data["plants"]]
        assert "KP01" in codes
        assert "KP02" in codes
        assert "KP03" in codes


# ── Helpers unit tests ────────────────────────────────────────────────────────
class TestHelpers:
    """Unit tests for delay bucket logic — no server needed."""

    def test_delay_bucket_on_time(self):
        from helpers import compute_delay_bucket
        from datetime import date, timedelta
        future = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
        result = compute_delay_bucket(future)
        assert result["delay_bucket"] == "On Time"
        assert result["status_icon"] == "Success"

    def test_delay_bucket_16_30(self):
        from helpers import compute_delay_bucket
        from datetime import date, timedelta
        past = (date.today() - timedelta(days=20)).strftime("%Y-%m-%d")
        result = compute_delay_bucket(past)
        assert result["delay_bucket"] == "16-30 Days"
        assert result["status_icon"] == "Warning"

    def test_delay_bucket_31_60(self):
        from helpers import compute_delay_bucket
        from datetime import date, timedelta
        past = (date.today() - timedelta(days=45)).strftime("%Y-%m-%d")
        result = compute_delay_bucket(past)
        assert result["delay_bucket"] == "31-60 Days"
        assert result["status_icon"] == "Error"

    def test_delay_bucket_over_60(self):
        from helpers import compute_delay_bucket
        from datetime import date, timedelta
        past = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
        result = compute_delay_bucket(past)
        assert result["delay_bucket"] == ">60 Days"
        assert result["status_icon"] == "Error"

    def test_delay_bucket_boundary_15(self):
        from helpers import compute_delay_bucket
        from datetime import date, timedelta
        boundary = (date.today() - timedelta(days=15)).strftime("%Y-%m-%d")
        result = compute_delay_bucket(boundary)
        assert result["delay_bucket"] == "On Time"

    def test_calculate_total(self):
        from helpers import calculate_total
        assert calculate_total(100, 1450.00) == 145000.00

    def test_apply_discount(self):
        from helpers import apply_discount
        result = apply_discount(100000.00, 10.0)
        assert result["discount_amount"] == 10000.00
        assert result["final_value"] == 90000.00
