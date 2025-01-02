from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.models.receipt import Receipt


class IReceiptService(ABC):
    @abstractmethod
    def create_receipt(self) -> Receipt:
        pass

    @abstractmethod
    def read_by_id_receipt(self, receipt_id: UUID) -> Optional[Receipt]:
        pass

    @abstractmethod
    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> Receipt:
        pass

    @abstractmethod
    def close_receipt(self, receipt_id: UUID) -> None:
        pass

    @abstractmethod
    def delete_receipt(self, receipt_id: UUID) -> None:
        pass

class ReceiptService(IReceiptService):
    def __init__(self, receipt_repo: ReceiptRepository):
        self.receipt_repo = receipt_repo

    def create_receipt(self) -> Receipt:
        return self.receipt_repo.open_receipt()

    def read_by_id_receipt(self, receipt_id: UUID) -> Optional[Receipt]:
        return self.receipt_repo.get_receipt(receipt_id)

    def close_receipt(self, receipt_id: UUID) -> None:
        self.receipt_repo.close_receipt(receipt_id)

    def delete_receipt(self, receipt_id: UUID) -> None:
        self.receipt_repo.delete_receipt(receipt_id)

    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> Receipt:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        rec: Optional[Receipt] = self.receipt_repo.get_receipt(receipt_id)
        if rec is None:
            raise ValueError("Receipt not found")
        if not rec.status:
            raise ValueError("Receipt is not open")
        return self.receipt_repo.add_product(receipt_id, product_id, quantity)