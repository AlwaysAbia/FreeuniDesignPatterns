import sqlite3
from decimal import Decimal
from typing import List
from uuid import UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.models.receipt import Receipt, ReceiptProduct


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
                (str(receipt.id), 1, str(receipt.total))
            )
            if self.db.connection is not None:
                self.db.connection.commit()
            return receipt
        except sqlite3.Error as e:
            if self.db.connection is not None:
                self.db.connection.rollback()
            raise e  # Re-raise the error so we can see what went wrong

    def close_receipt(self, receipt_id: UUID) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")

        try:
            # Update the status to CLOSED
            self.db.cursor.execute(
                "UPDATE Receipt SET status = ? WHERE id = ?",
                (0, str(receipt_id))
            )
            self.db.commit()  # Use the commit helper method
        except sqlite3.Error as e:
            self.db.rollback()  # Use the rollback helper method
            raise e  # Re-raise the exception for debugging/logging purposes

    def get_receipt(self, receipt_id: UUID) -> Receipt:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        # Fetch receipt details
        self.db.cursor.execute(
            "SELECT * FROM Receipt WHERE id = ?",
            (str(receipt_id),)
        )
        row = self.db.cursor.fetchone()
        if row is None:
            raise ValueError(f"Receipt with id {receipt_id} not found")
        # Parse receipt details
        id: UUID = UUID(row[0])
        status: bool = bool(row[1])
        total: Decimal = Decimal(row[2])
        item_list: List[ReceiptProduct] = []

        # Fetch receipt items
        self.db.cursor.execute(
            "SELECT * FROM Receipt_items WHERE receipt_id = ?",
            (str(receipt_id),)
        )
        rows = self.db.cursor.fetchall()
        for row in rows:
            item_list.append(
                ReceiptProduct(
                    product_id=UUID(row[1]),
                    quantity=row[2],
                    price_when_sold=Decimal(row[3])
                )
            )
        return Receipt(id=id, status=status, products=item_list, total=total)

    def add_product(self, receipt_id: UUID, product_id: UUID, quantity: int) -> Receipt:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")

        if self.db.cursor is None:
            raise RuntimeError("Database not connected")

        if not self.get_receipt_status(receipt_id):
            raise ValueError(
                f"Cannot add product to receipt {receipt_id}: Receipt is not open.")

        try:
            product = ProductRepository(self.db).read_product(product_id)
            existing_quantity = self.get_existing_quantity(receipt_id, product_id)

            if existing_quantity:
                # Update existing product quantity
                new_quantity = existing_quantity + quantity
                new_total = new_quantity * product.price
                self.update_receipt_item(receipt_id, product_id,
                                         new_quantity, new_total)
            else:
                # Add new product to receipt
                total = product.price * quantity
                self.insert_receipt_item(receipt_id, product_id, quantity,
                                         product.price, total)

            # Recalculate and update receipt total
            new_receipt_total = self.get_total(receipt_id)
            self.update_total(receipt_id, new_receipt_total)

            return self.get_receipt(receipt_id)

        except sqlite3.Error as e:
            if self.db.connection:
                self.db.connection.rollback()
            raise RuntimeError(f"Database error while adding product: {e}")

    #Helper Methods below this
    def get_total(self, receipt_id: UUID) -> Decimal:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT SUM(total) FROM Receipt_items WHERE receipt_id = ?",
            (str(receipt_id),)
        )
        row = self.db.cursor.fetchone()
        return Decimal(row[0]) if row and row[0] else Decimal(0)

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

    def update_receipt_item(self,
                            receipt_id: UUID, product_id: UUID,
                            quantity: int, total: Decimal) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            '''UPDATE Receipt_items SET quantity = ?, total = ? 
               WHERE receipt_id = ? AND product_id = ?''',
            (quantity, str(total), str(receipt_id), str(product_id))
        )

    def insert_receipt_item(self,
                            receipt_id: UUID, product_id: UUID,
                            quantity: int, price: Decimal, total: Decimal) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            '''INSERT INTO Receipt_items (receipt_id, product_id, 
            quantity, price_when_sold, total) 
            VALUES (?, ?, ?, ?, ?)''',
            (str(receipt_id), str(product_id), quantity, str(price), str(total))
        )

    def get_receipt_status(self, receipt_id: UUID) -> bool:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute("SELECT status FROM Receipt WHERE id = ?",
                               (str(receipt_id),))
        row = self.db.cursor.fetchone()
        if not row:
            raise ValueError(f"Receipt with ID {receipt_id} not found.")

        return bool(row[0])

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
            self.db.commit()  # Commit the changes
        except sqlite3.Error as e:
            self.db.rollback()
            raise e
        except ValueError as ve:
            raise ve  # Raise ValueError if input is invalid (like non-decimal total)