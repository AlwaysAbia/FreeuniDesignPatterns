#Model for the Receipt item
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4


class ReceiptStatus(Enum):
    OPEN = 'open'
    CLOSED = 'closed'

class ReceiptProduct:
    def __init__(self, product_id: UUID, quantity: int, price: Decimal):
        self.product_id : UUID = product_id
        self.quantity : int = quantity
        self.price : Decimal = price

    #For Testing
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReceiptProduct):
            return False
        return (self.product_id == other.product_id
                and self.quantity == other.quantity
                and self.price == other.price)

class Receipts:
    def __init__(self,  id: Optional[UUID] = None):
        self.id : UUID = id or uuid4()
        self.status : ReceiptStatus = ReceiptStatus.OPEN
        self.products : List[ReceiptProduct] = []

    #For Testing
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Receipts):
            return False
        return (self.id == other.id
                and self.status == other.status
                and self.products == other.products)