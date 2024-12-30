import sqlite3
from decimal import Decimal
from typing import List
from uuid import UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.models.product import Product


class ProductRepository:
    def __init__(self, database: Database) -> None:
        self.db = database

    def create_product(self, product: Product) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        try:
            self.db.cursor.execute(
                "INSERT INTO Product (id, unit_id, name, barcode, price) "
                "VALUES (?, ?, ?, ?, ?)",
                (str(product.id), str(product.unit_id),
                 product.name, product.barcode, str(product.price))
            )
            if self.db.connection is not None:
                self.db.connection.commit()
        except sqlite3.Error as e:
            if self.db.connection is not None:
                self.db.connection.rollback()
            raise e  # Re-raise the error so we can see what went wrong

    def read_product(self, product_id: UUID) -> Product:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT * FROM Product WHERE id = ?",
            (str(product_id),)
        )

        row = self.db.cursor.fetchone()  # Gets one row
        if row is None:
            raise ValueError(f"Product with id {product_id} not found")

        return Product(
            id=UUID(row[0]),
            unit_id=UUID(row[1]),
            name=row[2],
            barcode=row[3],
            price=Decimal(row[4])
        )

    def list_products(self) -> List[Product]:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT * FROM Product"
        )
        rows = self.db.cursor.fetchall()  # Gets all rows
        return [
            Product(
                id=UUID(row[0]),
                unit_id=UUID(row[1]),
                name=row[2],
                barcode=row[3],
                price=Decimal(row[4])
            ) for row in rows
        ]

    def update_product(self, product: Product, price: Decimal) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        if product is None:
            raise ValueError("Product cannot be None")
        try:
            self.db.cursor.execute(
                "UPDATE Product SET price = ? WHERE id = ?",
                (str(price), str(product.id))
            )
            if self.db.connection is not None:
                rows_affected = self.db.cursor.rowcount
                if rows_affected == 0:
                    raise ValueError(f"Product with id {product.id} not found")
                self.db.connection.commit()
        except sqlite3.Error as e:
            if self.db.connection is not None:
                self.db.connection.rollback()
            raise e