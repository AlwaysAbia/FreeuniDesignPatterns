#Model for the Receipt item
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4


class ReceiptProduct:
    def __init__(self, product_id: UUID, quantity: int,
                 price_when_sold: Decimal) -> None:
        self.product_id : UUID = product_id
        self.quantity : int = quantity
        self.price_when_sold : Decimal = price_when_sold

    #For Testing
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReceiptProduct):
            return False
        return (self.product_id == other.product_id
                and self.quantity == other.quantity
                and self.price_when_sold == other.price_when_sold)

class Receipt:
    def __init__(self,
                 id: Optional[UUID] = None,
                 status : bool = True,
                 products : Optional[List[ReceiptProduct]]=None,
                 total: Decimal = Decimal("0.00")) -> None:
        if products is None:
            products = []
        self.id : UUID = id or uuid4()
        self.status : bool = status
        self.products : List[ReceiptProduct] = products
        self.total: Decimal = total

    #For Testing
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Receipt):
            return False
        return (self.id == other.id
                and self.status == other.status
                and self.products == other.products)