import sqlite3
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, List
from uuid import UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import Receipt, ReceiptProduct


class IReceiptRepository(ABC):
    @abstractmethod
    def open_receipt(self) -> Receipt:
        pass

    @abstractmethod
    def close_receipt(self, receipt_id: UUID) -> None:
        pass

    @abstractmethod
    def get_receipt(self, receipt_id: UUID) -> Receipt:
        pass

    @abstractmethod
    def add_product(self, receipt_id: UUID,
                    product_id: UUID, quantity: int) -> Receipt:
        pass

    @abstractmethod
    def delete_receipt(self, receipt_id: UUID) -> None:
        pass

    @abstractmethod
    def get_receipt_status(self, receipt_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_total(self, receipt_id: UUID) -> Decimal:
        pass

class ReceiptRepository(IReceiptRepository):
   def __init__(self, database: Database) -> None:
       self.db = database

   def open_receipt(self) -> Receipt:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       try:
           receipt = Receipt()
           self.db.cursor.execute(
               "INSERT INTO Receipt (id, status, total) VALUES (?, ?, ?)",
               (str(receipt.id), 1, str(receipt.total))
           )
           self.db.commit()
           return receipt
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def close_receipt(self, receipt_id: UUID) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       try:
           self.db.cursor.execute(
               "UPDATE Receipt SET status = ? WHERE id = ?",
               (0, str(receipt_id))
           )
           self.db.commit()
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def get_receipt(self, receipt_id: UUID) -> Receipt:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       receipt_data = self._get_receipt_data(receipt_id)
       items = self._get_receipt_items(receipt_id)
       return Receipt(
           id=receipt_data['id'],
           status=receipt_data['status'],
           products=items,
           total=receipt_data['total']
       )

   def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> Receipt:
       self._validate_add_product(receipt_id, quantity)
       try:
           product = ProductRepository(self.db).read_product(product_id)
           existing_quantity = self.get_existing_quantity(receipt_id, product_id)

           if existing_quantity:
               self._update_existing_product(receipt_id, product_id, quantity, product)
           else:
               self._add_new_product(receipt_id, product_id, quantity, product)

           self._update_receipt_total(receipt_id)
           return self.get_receipt(receipt_id)

       except sqlite3.Error as e:
           self.db.rollback()
           raise RuntimeError(f"Database error while adding product: {e}")

   def delete_receipt(self, receipt_id: UUID) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       try:
           self.db.cursor.execute(
               "DELETE FROM Receipt_items WHERE receipt_id = ?",
               (str(receipt_id),)
           )
           self.db.cursor.execute(
               "DELETE FROM Receipt WHERE id = ?",
               (str(receipt_id),)
           )
           self.db.commit()
       except sqlite3.Error as e:
           self.db.rollback()
           raise RuntimeError(f"Error deleting receipt: {e}")

   def _get_receipt_data(self, receipt_id: UUID) -> Dict[str, Any]:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           "SELECT * FROM Receipt WHERE id = ?",
           (str(receipt_id),)
       )
       row = self.db.cursor.fetchone()
       if row is None:
           raise ValueError(f"Receipt with id {receipt_id} not found")

       return {
           'id': UUID(row[0]),
           'status': bool(row[1]),
           'total': Decimal(row[2])
       }

   def _get_receipt_items(self, receipt_id: UUID) -> List[ReceiptProduct]:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           "SELECT * FROM Receipt_items WHERE receipt_id = ?",
           (str(receipt_id),)
       )
       return [
           ReceiptProduct(
               product_id=UUID(row[1]),
               quantity=row[2],
               price_when_sold=Decimal(row[3])
           )
           for row in self.db.cursor.fetchall()
       ]

   def get_receipt_status(self, receipt_id: UUID) -> bool:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           "SELECT status FROM Receipt WHERE id = ?",
           (str(receipt_id),)
       )
       row = self.db.cursor.fetchone()
       if not row:
           raise ValueError(f"Receipt with ID {receipt_id} not found.")
       return bool(row[0])

   def _validate_add_product(self, receipt_id: UUID, quantity: int) -> None:
       if quantity <= 0:
           raise ValueError("Quantity must be greater than 0.")
       if not self.get_receipt_status(receipt_id):
           raise ValueError(
               f"Cannot add product to receipt {receipt_id}: Receipt is not open.")

   def _update_existing_product(self, receipt_id: UUID, product_id: UUID,
                               quantity: int, product: Product) -> None:
       existing_quantity = self.get_existing_quantity(receipt_id, product_id)
       new_quantity = existing_quantity + quantity
       new_total = new_quantity * product.price
       self.update_receipt_item(receipt_id, product_id, new_quantity, new_total)

   def _add_new_product(self, receipt_id: UUID, product_id: UUID,
                        quantity: int, product: Product) -> None:
       total = product.price * quantity
       self.insert_receipt_item(receipt_id, product_id, quantity, product.price, total)

   def get_existing_quantity(self, receipt_id: UUID, product_id: UUID) -> int:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           '''SELECT quantity FROM Receipt_items 
           WHERE receipt_id = ? AND product_id = ?''',
           (str(receipt_id), str(product_id))
       )
       row = self.db.cursor.fetchone()
       return row[0] if row else 0

   def update_receipt_item(self, receipt_id: UUID, product_id: UUID,
                          quantity: int, total: Decimal) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           '''UPDATE Receipt_items SET quantity = ?, total = ? 
              WHERE receipt_id = ? AND product_id = ?''',
           (quantity, str(total), str(receipt_id), str(product_id))
       )

   def insert_receipt_item(self, receipt_id: UUID, product_id: UUID,
                          quantity: int, price: Decimal, total: Decimal) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           '''INSERT INTO Receipt_items (receipt_id, product_id, 
           quantity, price_when_sold, total) 
           VALUES (?, ?, ?, ?, ?)''',
           (str(receipt_id), str(product_id), quantity, str(price), str(total))
       )

   def get_total(self, receipt_id: UUID) -> Decimal:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           "SELECT SUM(total) FROM Receipt_items WHERE receipt_id = ?",
           (str(receipt_id),)
       )
       row = self.db.cursor.fetchone()
       return Decimal(row[0]) if row and row[0] else Decimal(0)

   def update_total(self, receipt_id: UUID, new_total: Decimal) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       try:
           if not isinstance(new_total, Decimal):
               raise ValueError("New total must be a Decimal.")
           self.db.cursor.execute(
               "UPDATE Receipt SET total = ? WHERE id = ?",
               (str(new_total), str(receipt_id))
           )
           self.db.commit()
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def _update_receipt_total(self, receipt_id: UUID) -> None:
       new_receipt_total = self.get_total(receipt_id)
       self.update_total(receipt_id, new_receipt_total)