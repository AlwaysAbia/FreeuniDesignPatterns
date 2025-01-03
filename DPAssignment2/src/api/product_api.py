from decimal import Decimal
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.service.product_service import ProductService


# Pydantic models for request/response
class ProductCreate(BaseModel):
    name: str
    barcode: str
    price: Decimal

class ProductUpdate(BaseModel):
    id: UUID
    price: Decimal

class Product(BaseModel):
    id: UUID
    name: str
    unit_id: UUID
    barcode: str
    price: Decimal

class ProductResponse(BaseModel):
    product: Product

class ProductsResponse(BaseModel):
    products: List[Product]

class ErrorResponse(BaseModel):
    error: dict

#Create Router
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# Database dependency
def get_db():
    db = Database()
    db.connect()
    try:
        yield db
    finally:
        db.disconnect()

# Service dependency
def get_product_service(db: Database = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))