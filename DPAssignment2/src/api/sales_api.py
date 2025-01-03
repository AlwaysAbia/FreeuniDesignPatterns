from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.db_dependency import get_db
from DPAssignment2.src.db.repository.sales_repository import SalesRepository
from DPAssignment2.src.service.sales_service import SalesService


class SalesResponse(BaseModel):
    sales: dict[str, int | Decimal]

router: APIRouter = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

def get_sales_service(db: Database = Depends(get_db)) -> SalesService:
    return SalesService(SalesRepository(db))

@router.get("", response_model=SalesResponse)
async def get_sales_report(
    service: SalesService = Depends(get_sales_service)
) -> SalesResponse:
    return SalesResponse(sales={
        "n_receipts": service.get_n_receipts(),
        "revenue": service.get_revenue()
    })