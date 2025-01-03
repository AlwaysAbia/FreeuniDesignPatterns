from fastapi import FastAPI

from DPAssignment2.src.api.product_api import router as product_router
from DPAssignment2.src.api.receipt_api import router as receipt_router
from DPAssignment2.src.api.sales_api import router as sales_router
from DPAssignment2.src.api.unit_api import router as unit_router

app = FastAPI(title="POS System API")

# Include routers
app.include_router(unit_router)
app.include_router(product_router)
app.include_router(receipt_router)
app.include_router(sales_router)

# Optional: Add startup event to create tables
@app.on_event("startup")
async def startup_event() -> None:
    from DPAssignment2.src.db.database import Database
    db = Database()
    db.connect()
    db.create_tables()
    db.disconnect()