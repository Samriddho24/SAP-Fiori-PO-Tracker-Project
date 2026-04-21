"""
ZFI_PO_TRACKER — FastAPI Backend
KIIT Manufacturing Ltd. (KML) — SAP Fiori PO Delay Monitor
Student: Samriddho Kar | Roll No: 23053296 | B.Tech 2023-2027
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os
from helpers import compute_delay_bucket, apply_discount, calculate_total

app = FastAPI(
    title="ZFI_PO_TRACKER — KML Purchase Order API",
    description="SAP Fiori Fiori PO Delay Tracker for KIIT Manufacturing Ltd.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load sample data ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "o2c_data.json"), "r") as f:
    DATA = json.load(f)

PURCHASE_ORDERS = DATA.get("purchase_orders", [])
VENDORS         = DATA.get("vendors", [])
PLANTS          = DATA.get("plants", [])
SALES_ORDERS    = DATA.get("sales_orders", [])


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "app": "ZFI_PO_TRACKER",
        "company": "KIIT Manufacturing Ltd. (KML)",
        "version": "1.0.0",
    }


# ── Purchase Orders ───────────────────────────────────────────────────────────
@app.get("/purchase-orders", tags=["Purchase Orders"])
def list_purchase_orders(
    plant: Optional[str] = Query(None, description="Filter by plant code e.g. KP01"),
    vendor: Optional[str] = Query(None, description="Filter by vendor ID"),
    bucket: Optional[str] = Query(None, description="Filter by delay bucket"),
):
    """Return all purchase orders, optionally filtered, with computed delay buckets."""
    results = []
    for po in PURCHASE_ORDERS:
        po_copy = dict(po)
        delay_info = compute_delay_bucket(po_copy.get("delivery_date", ""))
        po_copy.update(delay_info)

        if plant and po_copy.get("plant") != plant:
            continue
        if vendor and po_copy.get("vendor_id") != vendor:
            continue
        if bucket and po_copy.get("delay_bucket") != bucket:
            continue

        results.append(po_copy)

    return {"total": len(results), "purchase_orders": results}


@app.get("/purchase-orders/delay-summary", tags=["Purchase Orders"])
def delay_summary():
    """Return KPI counts per delay bucket — used by the Fiori KPI strip."""
    summary = {
        "On Time":    0,
        "16-30 Days": 0,
        "31-60 Days": 0,
        ">60 Days":   0,
        "total":      len(PURCHASE_ORDERS),
    }
    for po in PURCHASE_ORDERS:
        info = compute_delay_bucket(po.get("delivery_date", ""))
        bucket = info.get("delay_bucket", "On Time")
        if bucket in summary:
            summary[bucket] += 1
    return summary


@app.get("/purchase-orders/{po_number}", tags=["Purchase Orders"])
def get_purchase_order(po_number: str):
    """Return a single PO by PO number with full item detail."""
    for po in PURCHASE_ORDERS:
        if po.get("po_number") == po_number:
            po_copy = dict(po)
            delay_info = compute_delay_bucket(po_copy.get("delivery_date", ""))
            po_copy.update(delay_info)

            # Enrich items with line totals
            items = po_copy.get("items", [])
            for item in items:
                item["line_total"] = calculate_total(
                    item.get("quantity", 0), item.get("unit_price", 0)
                )
                item.update(delay_info)

            po_copy["items"] = items
            return po_copy

    raise HTTPException(status_code=404, detail=f"PO {po_number} not found")


@app.post("/purchase-orders/filter", tags=["Purchase Orders"])
def filter_purchase_orders(filters: dict):
    """
    Advanced filter — accepts JSON body:
    { "plant": "KP01", "vendor_id": "V00421", "bucket": "31-60 Days" }
    """
    results = []
    for po in PURCHASE_ORDERS:
        po_copy = dict(po)
        delay_info = compute_delay_bucket(po_copy.get("delivery_date", ""))
        po_copy.update(delay_info)

        match = True
        for key, value in filters.items():
            if key == "bucket":
                if po_copy.get("delay_bucket") != value:
                    match = False
            elif po_copy.get(key) != value:
                match = False

        if match:
            results.append(po_copy)

    return {"total": len(results), "purchase_orders": results}


# ── Vendors ───────────────────────────────────────────────────────────────────
@app.get("/vendors", tags=["Master Data"])
def list_vendors():
    """Return KML vendor master list."""
    return {"total": len(VENDORS), "vendors": VENDORS}


# ── Plants ────────────────────────────────────────────────────────────────────
@app.get("/plants", tags=["Master Data"])
def list_plants():
    """Return KML plant master list."""
    return {"total": len(PLANTS), "plants": PLANTS}


# ── Sales Orders (O2C) ────────────────────────────────────────────────────────
@app.get("/sales-orders", tags=["Sales Orders"])
def list_sales_orders(customer: Optional[str] = Query(None)):
    """Return KML sales orders, optionally filtered by customer."""
    results = SALES_ORDERS
    if customer:
        results = [so for so in SALES_ORDERS if so.get("customer_id") == customer]
    return {"total": len(results), "sales_orders": results}


# ── O2C Process Steps ─────────────────────────────────────────────────────────
@app.get("/o2c/steps", tags=["Process"])
def o2c_steps():
    """Return Order-to-Cash process steps for KML."""
    return DATA.get("o2c_steps", [])


# ── P2P Process Steps ─────────────────────────────────────────────────────────
@app.get("/p2p/steps", tags=["Process"])
def p2p_steps():
    """Return Procure-to-Pay process steps for KML."""
    return DATA.get("p2p_steps", [])
