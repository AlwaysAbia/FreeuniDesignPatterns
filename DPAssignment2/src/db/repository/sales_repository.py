from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any

from DPAssignment2.src.db.database import Database


class ISalesRepository(ABC):
    @abstractmethod
    def get_n_receipts(self) -> int:
        pass

    @abstractmethod
    def get_revenue(self) -> Decimal:
        pass

class SalesRepository(ISalesRepository):
   def __init__(self, database: Database) -> None:
       self.db = database

   def _execute_query(self, query: str, params: tuple[Any, ...] = ()) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(query, params)

   def get_n_receipts(self) -> int:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute("SELECT COUNT(id) FROM Receipt")
       row = self.db.cursor.fetchone()
       if row is None or row[0] is None:
           return 0
       return int(row[0])

   def get_revenue(self) -> Decimal:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute("SELECT SUM(total) FROM Receipt")
       row = self.db.cursor.fetchone()
       return Decimal(row[0]) if row and row[0] else Decimal(0)