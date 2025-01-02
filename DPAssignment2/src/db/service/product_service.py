from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.models.product import Product


class IProductService(ABC):
    @abstractmethod
    def create_product(self, name: str, unit_id: UUID,
                       barcode: str, price: Decimal) -> Product:
        pass

    @abstractmethod
    def read_product(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def list_products(self) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, product_id: UUID, price: Decimal) -> None:
        pass

class ProductService(IProductService):
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def create_product(self, name: str, unit_id: UUID,
                       barcode: str, price: Decimal) -> Product:
        if name == "":
            raise ValueError("Name cannot be an empty string")
        if barcode == "":
            raise ValueError("Barcode cannot be an empty string")
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        return self.product_repo.create_product(name, unit_id, barcode, price)

    def read_product(self, product_id: UUID) -> Optional[Product]:
        return self.product_repo.read_product(product_id)

    def list_products(self) -> List[Product]:
        return self.product_repo.list_products()

    def update_product(self, product_id: UUID, price: Decimal) -> None:
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        self.product_repo.update_product(product_id, price)