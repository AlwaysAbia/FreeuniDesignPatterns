import sqlite3
from uuid import uuid4, UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import ReceiptStatus, Receipt, ReceiptProduct


class ReceiptRepository:
    def __init__(self, database: Database) -> None:
        self.db = database

    def open_receipt(self) -> Receipt:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        try:
            receipt : Receipt = Receipt()
            self.db.cursor.execute(
                "INSERT INTO Receipt (id, status, total) VALUES (?, ?, ?)",
                (str(receipt.id), receipt.status, str(receipt.total))
            )
            if self.db.connection is not None:
                self.db.connection.commit()
            return receipt
        except sqlite3.Error as e:
            if self.db.connection is not None:
                self.db.connection.rollback()
            raise e  # Re-raise the error so we can see what went wrong

    def get_receipt_status(self, receipt_id: UUID) -> ReceiptStatus:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute("SELECT status FROM Receipt WHERE id = ?",
                               (str(receipt_id),))
        row = self.db.cursor.fetchone()
        if not row:
            raise ValueError(f"Receipt with ID {receipt_id} not found.")
        return ReceiptStatus(row[0])

    def close_receipt(self, receipt_id: UUID) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")

        try:
            # Update the status to CLOSED
            self.db.cursor.execute(
                "UPDATE Receipt SET status = ? WHERE id = ?",
                (ReceiptStatus.CLOSED, str(receipt_id))
            )
            self.db.commit()  # Use the commit helper method
        except sqlite3.Error as e:
            self.db.rollback()  # Use the rollback helper method
            raise e  # Re-raise the exception for debugging/logging purposes

    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")

        status = self.get_receipt_status(receipt_id)
        if status != ReceiptStatus.OPEN:
            raise ValueError(
                f"Cannot add product to receipt {receipt_id}: Receipt is not open."
            )

        try:
            pr: ProductRepository = ProductRepository(self.db)
            product: Product = pr.read_product(product_id)
            self.db.cursor.execute(
                '''INSERT INTO Receipt_items 
                (receipt_id, product_id, quantity, price_when_sold, total) 
                VALUES (?, ?, ?, ?, ?)''',
                (str(receipt_id), str(product_id),
                 quantity, str(product.price), str(product.price*quantity))
            )
            self.db.commit()
        except sqlite3.Error as e:
            self.db.rollback()
            raise e  # Re-raise the error so we can see what went wrong
