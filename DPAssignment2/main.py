from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

from DPAssignment2.src.api.product_api import router as product_router
from DPAssignment2.src.api.receipt_api import router as receipt_router
from DPAssignment2.src.api.sales_api import router as sales_router
from DPAssignment2.src.api.unit_api import router as unit_router
from DPAssignment2.src.db.db_dependency import DatabaseManager, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DatabaseManager.get_instance()
    db.connect()
    db.create_tables()
    yield
    db.disconnect()

app = FastAPI(title="POS System API", lifespan=lifespan)

app.include_router(unit_router, dependencies=[Depends(get_db)])
app.include_router(product_router, dependencies=[Depends(get_db)])
app.include_router(receipt_router, dependencies=[Depends(get_db)])
app.include_router(sales_router, dependencies=[Depends(get_db)])