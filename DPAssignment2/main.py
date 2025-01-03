from fastapi import FastAPI
from DPAssignment2.src.api.unit_api import router as unit_router
from DPAssignment2.src.api.product_api import router as product_router

app = FastAPI(title="POS System API")

# Include routers
app.include_router(unit_router)
app.include_router(product_router)

# Optional: Add startup event to create tables
@app.on_event("startup")
async def startup_event():
    from DPAssignment2.src.db.database import Database
    db = Database()
    db.connect()
    db.create_tables()
    db.disconnect()