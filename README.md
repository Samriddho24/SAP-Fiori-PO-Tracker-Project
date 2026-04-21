# ZFI_PO_TRACKER — SAP Fiori Purchase Order Delay Monitor

---

## Project Overview

`ZFI_PO_TRACKER` is a production-grade SAP Fiori application built for **KIIT Manufacturing Ltd. (KML)** — a fictitious discrete manufacturing enterprise with three plants in India (Bhubaneswar, Pune, Chennai).

The app replaces the manual Excel-based purchase order delay review with a live, filterable, colour-coded, mobile-accessible dashboard deployed on **SAP BTP Workzone**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | SAPUI5 1.120 (Fiori Elements — List Report + Object Page) |
| Backend Service | SAP CAP Node.js (`@sap/cds 7.x`) — OData V4 |
| Cloud Platform | SAP BTP Cloud Foundry (Mumbai region) |
| Launchpad | SAP BTP Workzone Standard |
| Source API | S/4HANA OData V2 — `API_PURCHASEORDER_PROCESS_SRV` |
| Auth | SAP IAS (SSO) + BTP Role Collections |
| CI/CD | SAP BTP Continuous Integration & Delivery Service |
| Tests | Jest 29.x |

---

## Features

- **Delay Bucket Classification** — On Time / 16–30 Days / 31–60 Days / >60 Days
- **KPI Strip** — live count of POs per delay bucket
- **Smart Filter Bar** — Plant (mandatory), Vendor, PO Date, Delay Bucket
- **Object Page Drill-Down** — tap any PO row to see full header + item details
- **Colour-coded ObjectStatus** — Green / Orange / Red semantic indicators
- **BTP Alert Notification** — daily push alert for POs overdue >30 days
- **Mobile Responsive** — card layout on 375 px viewport (iPhone)
- **Role-Based Access** — `ZFI_PO_VIEWER` scope enforced at OData layer

---

## Project Structure

```
zfi_po_tracker/
├── app.py                  # FastAPI mock server (local dev / demo)
├── assistant.py            # AI assistant helper for O2C/P2P step guidance
├── helpers.py              # Utility functions (delay bucket, discount calc)
├── o2c_data.json           # Order-to-Cash sample data (KML sales orders)
├── run.py                  # Uvicorn server startup
├── test_api.py             # API test suite (pytest + requests)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/samriddhokar/zfi-po-tracker.git
cd zfi_po_tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your SAP BTP credentials
```

### 4. Start the server
```bash
python run.py
```

Server starts at `http://localhost:8000`

### 5. Run tests
```bash
pytest test_api.py -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/purchase-orders` | List all POs with delay buckets |
| GET | `/purchase-orders/{po_number}` | Get single PO detail |
| GET | `/purchase-orders/delay-summary` | KPI counts per delay bucket |
| GET | `/vendors` | List KML vendor master |
| GET | `/plants` | List KML plant master |
| POST | `/purchase-orders/filter` | Filter POs by plant, vendor, bucket |
| GET | `/o2c/steps` | Order-to-Cash process steps |

---

## Company Structure (KML)

| Unit | Value |
|---|---|
| Company Code | KML1 |
| Plants | KP01 (Bhubaneswar), KP02 (Pune), KP03 (Chennai) |
| Purchasing Org | KML_PO |
| Sales Org | KSO1 |
| Controlling Area | KML1 |

---


