#Model for the Product item
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


class Product:
    def __init__(self,
                name: str,
                unit_id: UUID,
                barcode: str,
                price: Decimal,
                id: Optional[UUID] = None) -> None:
        self.id : UUID = id or uuid4()
        self.name : str = name
        self.unit_id : UUID = unit_id
        self.barcode : str = barcode
        self.price : Decimal = price

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return False
        return (self.id == other.id
                and self.name == other.name
                and self.unit_id == other.unit_id
                and self.barcode == other.barcode
                and self.price == other.price)