from decimal import Decimal

from DPAssignment2.src.db.database import Database


class SalesRepository:
    def __init__(self, database: Database):
        self.db = database

    def get_n_receipts(self) -> int:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT COUNT(id) FROM Receipt",
        )
        row = self.db.cursor.fetchone()
        return row[0]

    def get_revenue(self) -> Decimal:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT SUM(total) FROM Receipt"
        )
        row = self.db.cursor.fetchone()
        return Decimal(row[0]) if row and row[0] else Decimal(0)
