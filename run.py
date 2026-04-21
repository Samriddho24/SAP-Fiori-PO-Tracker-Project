"""
run.py — Uvicorn server startup for ZFI_PO_TRACKER
Student: Samriddho Kar | Roll No: 23053296
"""

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("ENV", "development") == "development"

    print(f"Starting ZFI_PO_TRACKER server on {host}:{port}")
    print("Company: KIIT Manufacturing Ltd. (KML)")
    print(f"Docs: http://localhost:{port}/docs")

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
