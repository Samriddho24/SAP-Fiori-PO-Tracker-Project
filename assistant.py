"""
assistant.py — SAP Process Assistant for ZFI_PO_TRACKER
Refactored O2C and P2P steps into structured format
Student: Samriddho Kar | Roll No: 23053296
"""

from typing import List, Dict


# ── Order-to-Cash (O2C) Steps ─────────────────────────────────────────────────
O2C_STEPS: List[Dict] = [
    {
        "step": 1,
        "phase": "Sales Inquiry",
        "tcode": "VA11",
        "description": "Customer contacts KML with a product inquiry. Sales rep creates an inquiry document in SAP SD.",
        "deliverable": "Inquiry document (document type IN)",
        "role": "Sales Representative",
    },
    {
        "step": 2,
        "phase": "Sales Quotation",
        "tcode": "VA21",
        "description": "Sales rep generates a formal quotation with pricing, delivery terms, and validity period.",
        "deliverable": "Quotation document (document type QT)",
        "role": "Sales Representative",
    },
    {
        "step": 3,
        "phase": "Sales Order",
        "tcode": "VA01",
        "description": "Customer confirms the quotation. Sales rep creates a sales order referencing the quotation. Credit check runs automatically.",
        "deliverable": "Sales order (document type OR)",
        "role": "Sales Representative",
    },
    {
        "step": 4,
        "phase": "Delivery Creation",
        "tcode": "VL01N",
        "description": "Warehouse creates an outbound delivery referencing the sales order. Picking and packing instructions are generated.",
        "deliverable": "Outbound delivery document",
        "role": "Warehouse Manager",
    },
    {
        "step": 5,
        "phase": "Goods Issue",
        "tcode": "VL02N",
        "description": "Warehouse posts goods issue — stock is reduced and cost of goods sold is posted to FI-CO.",
        "deliverable": "Material document + accounting document",
        "role": "Warehouse Manager",
    },
    {
        "step": 6,
        "phase": "Billing",
        "tcode": "VF01",
        "description": "Billing clerk creates an invoice referencing the delivery. Customer account is debited in AR.",
        "deliverable": "Customer invoice (billing document)",
        "role": "Billing Clerk",
    },
    {
        "step": 7,
        "phase": "Payment Receipt",
        "tcode": "F-28",
        "description": "Finance posts incoming payment from the customer, clearing the open AR item.",
        "deliverable": "Payment clearing document",
        "role": "Accounts Receivable",
    },
]


# ── Procure-to-Pay (P2P) Steps ────────────────────────────────────────────────
P2P_STEPS: List[Dict] = [
    {
        "step": 1,
        "phase": "Purchase Requisition",
        "tcode": "ME51N",
        "description": "Plant or MRP raises a purchase requisition for materials needed at KML plants.",
        "deliverable": "Purchase Requisition (PR)",
        "role": "Plant Planner / MRP",
    },
    {
        "step": 2,
        "phase": "Request for Quotation",
        "tcode": "ME41",
        "description": "Buyer sends RFQ to shortlisted vendors. Vendors submit quotations.",
        "deliverable": "RFQ document",
        "role": "Buyer (KML_PO)",
    },
    {
        "step": 3,
        "phase": "Vendor Comparison",
        "tcode": "ME49",
        "description": "Buyer compares vendor quotations on price, delivery date, and payment terms using the price comparison list.",
        "deliverable": "Price comparison list",
        "role": "Buyer (KML_PO)",
    },
    {
        "step": 4,
        "phase": "Purchase Order",
        "tcode": "ME21N",
        "description": "Buyer creates a purchase order for the selected vendor. Approval workflow triggers for POs above threshold.",
        "deliverable": "Purchase Order (PO)",
        "role": "Buyer / Manager",
    },
    {
        "step": 5,
        "phase": "Goods Receipt",
        "tcode": "MIGO",
        "description": "Warehouse posts goods receipt against the PO. Stock increases and GR/IR account is credited.",
        "deliverable": "Material document",
        "role": "Warehouse (KML Plants)",
    },
    {
        "step": 6,
        "phase": "Invoice Verification",
        "tcode": "MIRO",
        "description": "AP clerk posts vendor invoice. 3-way match: PO qty = GR qty = Invoice qty. Tolerances checked.",
        "deliverable": "Invoice document",
        "role": "Accounts Payable",
    },
    {
        "step": 7,
        "phase": "Payment",
        "tcode": "F110",
        "description": "Automatic payment run pays vendor as per payment terms. Bank posting created.",
        "deliverable": "Payment document",
        "role": "Treasury / AP",
    },
]


def get_o2c_steps() -> List[Dict]:
    """Return all Order-to-Cash process steps."""
    return O2C_STEPS


def get_p2p_steps() -> List[Dict]:
    """Return all Procure-to-Pay process steps."""
    return P2P_STEPS


def get_step_by_tcode(tcode: str) -> Dict:
    """Look up a process step by SAP transaction code."""
    all_steps = O2C_STEPS + P2P_STEPS
    for step in all_steps:
        if step.get("tcode", "").upper() == tcode.upper():
            return step
    return {"error": f"No step found for T-code {tcode}"}


def explain_delay_bucket(bucket: str) -> str:
    """Return a plain-language explanation of a delay bucket."""
    explanations = {
        "On Time":    "Delivery date is within 15 days from today. No action required.",
        "16-30 Days": "Delivery is 16 to 30 days overdue. Consider contacting the vendor for an ETA update.",
        "31-60 Days": "Delivery is 31 to 60 days overdue. Escalate to vendor account manager and review alternative sourcing.",
        ">60 Days":   "Delivery is more than 60 days overdue. Immediate escalation required. Consider emergency purchase or alternate vendor.",
    }
    return explanations.get(bucket, "Unknown delay bucket.")
