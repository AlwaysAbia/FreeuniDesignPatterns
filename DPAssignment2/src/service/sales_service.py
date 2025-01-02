from abc import ABC, abstractmethod
from decimal import Decimal

from DPAssignment2.src.db.repository.sales_repository import SalesRepository


class ISalesService(ABC):
    @abstractmethod
    def get_n_receipts(self) -> int:
        pass

    @abstractmethod
    def get_revenue(self) -> Decimal:
        pass

class SalesService(ISalesService):
    def __init__(self, sales_repo: SalesRepository):
        self.sales_repo = sales_repo

    def get_n_receipts(self) -> int:
        return self.sales_repo.get_n_receipts()

    def get_revenue(self) -> Decimal:
        return self.sales_repo.get_revenue()