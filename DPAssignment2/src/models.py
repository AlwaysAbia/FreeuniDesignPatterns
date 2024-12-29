from decimal import Decimal
from enum import Enum
from typing import List
from uuid import uuid4, UUID

#Model for the Unit item
class Unit:
    def __init__(self, name: str, id: UUID = None):
        self.id : UUID = id or uuid4()
        self.name : str = name

#Model for the Product item
class Product:
    def __init__(self,
                name: str,
                unit_id: UUID,
                barcode: str,
                price: Decimal,
                id: UUID = None):
        self.id : UUID = id or uuid4()
        self.name : str = name
        self.unit_id : UUID = unit_id
        self.barcode : str = barcode
        self.price : Decimal = price

#Model for the Receipt item
class ReceiptStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'

class ReceiptProduct:
    def __init__(self, product_id: UUID, quantity: int, price: Decimal):
        self.product_id : UUID = product_id
        self.quantity : int = quantity
        self.price : Decimal = price

class Receipts:
    def __init__(self,  id: UUID = None):
        self.id : UUID = id or uuid4()
        self.status : ReceiptStatus = ReceiptStatus.OPEN
        self.products : List[ReceiptProduct] = []
