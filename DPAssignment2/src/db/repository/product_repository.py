import sqlite3
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    def create_product(self, name: str, unit_id: UUID,
                       barcode: str, price: Decimal) -> Product:
        pass

    @abstractmethod
    def read_product(self, product_id: UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def list_products(self) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, product_id: UUID, price: Decimal) -> None:
        pass

class ProductRepository(IProductRepository):
   def __init__(self, database: Database) -> None:
       self.db = database

   def create_product(self, name: str, unit_id: UUID,
                      barcode: str, price: Decimal) -> Product:
       product_id = uuid4()
       try:
           if self.db.cursor is None:
               raise RuntimeError("Database not connected")
           self.db.cursor.execute(
               '''INSERT INTO Product 
               (id, unit_id, name, barcode, price) VALUES (?, ?, ?, ?, ?)''',
               (str(product_id), str(unit_id), name, barcode, str(price))
           )
           self.db.commit()
           return Product(id=product_id, unit_id=unit_id,
                          name=name, barcode=barcode, price=price)
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def read_product(self, product_id: UUID) -> Optional[Product]:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(
           "SELECT * FROM Product WHERE id = ?", (str(product_id),))
       row = self.db.cursor.fetchone()
       if row is None:
           return None
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
       self.db.cursor.execute("SELECT * FROM Product")
       return [Product(
           id=UUID(row[0]),
           unit_id=UUID(row[1]),
           name=row[2],
           barcode=row[3],
           price=Decimal(row[4])
       ) for row in self.db.cursor.fetchall()]

   def update_product(self, product_id: UUID, price: Decimal) -> None:
       try:
           if self.db.cursor is None:
               raise RuntimeError("Database not connected")
           self.db.cursor.execute(
               "UPDATE Product SET price = ? WHERE id = ?",
               (str(price), str(product_id))
           )
           if self.db.cursor.rowcount == 0:
               raise ValueError(f"Product with id {product_id} not found")
           self.db.commit()
       except sqlite3.Error as e:
           self.db.rollback()
           raise e