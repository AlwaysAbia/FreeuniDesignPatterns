import sqlite3
from typing import Optional


class Database:
    def __init__(self, db_name: str = "database.db"):
        self.db_name : str = db_name
        self.connection : Optional[sqlite3.Connection] = None
        self.cursor : Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        # Initialize connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self) -> None:
        # Close connection safely
        if self.connection is not None:
            self.connection.close()

    def create_tables(self) -> None:
        if self.cursor is None:
            raise RuntimeError("Database not connected. Call connect() first.")

        # Units table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Unit (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                id TEXT PRIMARY KEY,
                unit_id TEXT NOT NULL,
                name TEXT NOT NULL,
                barcode TEXT UNIQUE NOT NULL,
                price INTEGER NOT NULL,
                FOREIGN KEY (unit_id) REFERENCES Unit (id)
            )
        ''')

        # Receipts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Receipt (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                total INTEGER NOT NULL
            )
        ''')

        # Receipt items table (junction table)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Receipt_items (
                receipt_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price_when_sold INTEGER NOT NULL,
                total INTEGER NOT NULL,
                PRIMARY KEY (receipt_id, product_id),
                FOREIGN KEY (receipt_id) REFERENCES Receipt (id),
                FOREIGN KEY (product_id) REFERENCES Product (id)
            )
        ''')