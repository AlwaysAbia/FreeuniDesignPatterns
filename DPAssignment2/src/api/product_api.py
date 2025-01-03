from decimal import Decimal
from typing import Generator, List, Optional, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.models.product import Product as ProductModel
from DPAssignment2.src.service.product_service import ProductService


class ProductCreate(BaseModel):
    name: str
    unit_id: UUID
    barcode: str
    price: Decimal

class ProductUpdate(BaseModel):
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
    error: dict[str, str]

router: APIRouter = APIRouter(
    prefix="/products",
    tags=["products"]
)

def get_db() -> Generator[Database, None, None]:
    db: Database = Database()
    db.connect()
    try:
        yield db
    finally:
        db.disconnect()

def get_product_service(db: Database = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))

@router.post("", response_model=ProductResponse, status_code=201,
             responses={409: {"model": ErrorResponse}})
async def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    try:
        product: ProductModel = service.create_product(
            name=product_data.name,
            unit_id=product_data.unit_id,
            barcode=product_data.barcode,
            price=product_data.price
        )
        return ProductResponse(product=Product(
            id=product.id,
            unit_id=product.unit_id,
            name=product.name,
            barcode=product.barcode,
            price=product.price
        ))
    except ValueError as e:
        raise HTTPException(status_code=409, detail={"message": str(e)})

@router.get("/{product_id}", response_model=ProductResponse,
            responses={404: {"model": ErrorResponse}})
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    product: Optional[ProductModel] = service.read_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail={"message": f"Product with id<{product_id}> does not exist."}
        )
    return ProductResponse(product=Product(
        id=product.id,
        unit_id=product.unit_id,
        name=product.name,
        barcode=product.barcode,
        price=product.price
    ))

@router.get("", response_model=ProductsResponse)
async def list_products(
    service: ProductService = Depends(get_product_service)
) -> ProductsResponse:
    products: List[ProductModel] = service.list_products()
    return ProductsResponse(products=[
        Product(
            id=p.id,
            unit_id=p.unit_id,
            name=p.name,
            barcode=p.barcode,
            price=p.price
        ) for p in products
    ])

@router.patch("/{product_id}", response_model=None,
              responses={404: {"model": ErrorResponse}})
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
) -> dict[str, Any]:
    try:
        service.update_product(product_id, product_data.price)
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"message": str(e)})
    return {}