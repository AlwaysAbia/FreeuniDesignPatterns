from decimal import Decimal
from DPAssignment2.src.db.database import Database

class SalesRepository:
    def __init__(self, database: Database):
        self.db = database

    def _ensure_connection(self) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")

    def _execute_query(self, query: str, params: tuple = ()) -> None:
        self._ensure_connection()
        self.db.cursor.execute(query, params)

    def get_n_receipts(self) -> int:
        self._execute_query("SELECT COUNT(id) FROM Receipt")
        return self.db.cursor.fetchone()[0]

    def get_revenue(self) -> Decimal:
        self._execute_query("SELECT SUM(total) FROM Receipt")
        row = self.db.cursor.fetchone()
        return Decimal(row[0]) if row and row[0] else Decimal(0)