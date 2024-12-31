import sqlite3
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4
from DPAssignment2.src.db.database import Database
from DPAssignment2.src.models.product import Product

class ProductRepository:
   def __init__(self, database: Database) -> None:
       self.db = database

   def _ensure_connection(self) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")

   def _execute_query(self, query: str, params: tuple) -> None:
       self._ensure_connection()
       self.db.cursor.execute(query, params)

   def create_product(self, name: str, unit_id: UUID, barcode: str, price: Decimal) -> Product:
       product_id = uuid4()
       try:
           self._execute_query(
               "INSERT INTO Product (id, unit_id, name, barcode, price) VALUES (?, ?, ?, ?, ?)",
               (str(product_id), str(unit_id), name, barcode, str(price))
           )
           self.db.commit()
           return Product(id=product_id, unit_id=unit_id, name=name, barcode=barcode, price=price)
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def read_product(self, product_id: UUID) -> Product:
       self._execute_query("SELECT * FROM Product WHERE id = ?", (str(product_id),))
       row = self.db.cursor.fetchone()
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
       self._execute_query("SELECT * FROM Product", ())
       return [Product(
           id=UUID(row[0]),
           unit_id=UUID(row[1]),
           name=row[2],
           barcode=row[3],
           price=Decimal(row[4])
       ) for row in self.db.cursor.fetchall()]

   def update_product(self, product: Product, price: Decimal) -> None:
       if product is None:
           raise ValueError("Product cannot be None")
       try:
           self._execute_query(
               "UPDATE Product SET price = ? WHERE id = ?",
               (str(price), str(product.id))
           )
           if self.db.cursor.rowcount == 0:
               raise ValueError(f"Product with id {product.id} not found")
           self.db.commit()
       except sqlite3.Error as e:
           self.db.rollback()
           raise e