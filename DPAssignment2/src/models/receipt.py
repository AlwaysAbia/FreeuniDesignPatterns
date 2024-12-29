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

class Receipts:
    def __init__(self,  id: Optional[UUID] = None):
        self.id : UUID = id or uuid4()
        self.status : ReceiptStatus = ReceiptStatus.OPEN
        self.products : List[ReceiptProduct] = []
