from decimal import Decimal
from typing import Any, Generator, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.models.receipt import Receipt as ReceiptModel
from DPAssignment2.src.service.receipt_service import ReceiptService


class ReceiptProduct(BaseModel):
    product_id: UUID
    quantity: int
    price_when_sold: Decimal

    @property
    def total(self) -> Decimal:
        return self.price_when_sold * self.quantity


class Receipt(BaseModel):
    id: UUID
    status: bool
    products: List[ReceiptProduct]
    total: Decimal


class ReceiptResponse(BaseModel):
    receipt: Receipt


class AddProduct(BaseModel):
    id: UUID
    quantity: int


class ErrorResponse(BaseModel):
    error: dict[str, str]


router: APIRouter = APIRouter(
    prefix="/receipts",
    tags=["receipts"]
)


def get_db() -> Generator[Database, None, None]:
    db: Database = Database()
    db.connect()
    try:
        yield db
    finally:
        db.disconnect()


def get_receipt_service(db: Database = Depends(get_db)) -> ReceiptService:
    return ReceiptService(ReceiptRepository(db))


@router.post("", response_model=ReceiptResponse, status_code=201)
async def create_receipt(
        service: ReceiptService = Depends(get_receipt_service)
) -> ReceiptResponse:
    receipt: ReceiptModel = service.create_receipt()
    return ReceiptResponse(receipt=Receipt(
        id=receipt.id,
        status=receipt.status,
        products=[],
        total=receipt.total
    ))


@router.post("/{receipt_id}/products", response_model=ReceiptResponse, status_code=201,
             responses={404: {"model": ErrorResponse}})
async def add_product(
        receipt_id: UUID,
        product_data: AddProduct,
        service: ReceiptService = Depends(get_receipt_service)
) -> ReceiptResponse:
    try:
        receipt: ReceiptModel = service.add_product(
            receipt_id=receipt_id,
            product_id=product_data.id,
            quantity=product_data.quantity
        )
        return ReceiptResponse(receipt=Receipt(
            id=receipt.id,
            status=receipt.status,
            products=[
                ReceiptProduct(
                    product_id=p.product_id,
                    quantity=p.quantity,
                    price_when_sold=p.price_when_sold
                ) for p in receipt.products
            ],
            total=receipt.total
        ))
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"message": str(e)})


@router.get("/{receipt_id}", response_model=ReceiptResponse,
            responses={404: {"model": ErrorResponse}})
async def get_receipt(
        receipt_id: UUID,
        service: ReceiptService = Depends(get_receipt_service)
) -> ReceiptResponse:
    receipt: Optional[ReceiptModel] = service.read_by_id_receipt(receipt_id)
    if receipt is None:
        raise HTTPException(
            status_code=404,
            detail={"message": f"Receipt with id<{receipt_id}> does not exist."}
        )
    return ReceiptResponse(receipt=Receipt(
        id=receipt.id,
        status=receipt.status,
        products=[
            ReceiptProduct(
                product_id=p.product_id,
                quantity=p.quantity,
                price_when_sold=p.price_when_sold
            ) for p in receipt.products
        ],
        total=receipt.total
    ))


@router.patch("/{receipt_id}", response_model=None,
              responses={404: {"model": ErrorResponse}})
async def close_receipt(
        receipt_id: UUID,
        service: ReceiptService = Depends(get_receipt_service)
) -> dict[str, Any]:
    try:
        service.close_receipt(receipt_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"message": str(e)})
    return {}


@router.delete("/{receipt_id}", response_model=None,
               responses={404: {"model": ErrorResponse}})
async def delete_receipt(
        receipt_id: UUID,
        service: ReceiptService = Depends(get_receipt_service)
) -> dict[str, Any]:
    try:
        service.delete_receipt(receipt_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"message": str(e)})
    return {}