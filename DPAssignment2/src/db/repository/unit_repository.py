import sqlite3
from typing import List
from uuid import UUID

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.models.unit import Unit


class UnitRepository:
    def __init__(self, database: Database) -> None:
        self.db = database

    def create_unit(self, unit: Unit) -> None:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        try:
            self.db.cursor.execute(
                "INSERT INTO Unit (id, name) VALUES (?, ?)",
                (str(unit.id), unit.name)
            )
            if self.db.connection is not None:
                self.db.connection.commit()
        except sqlite3.Error as e:
            if self.db.connection is not None:
                self.db.connection.rollback()
            raise e  # Re-raise the error so we can see what went wrong

    def read_unit(self, unit_id: UUID) -> Unit:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT * FROM Unit WHERE id = ?",
            (str(unit_id),)
        )

        row = self.db.cursor.fetchone()  # Gets one row
        if row is None:
            raise ValueError(f"Unit with id {unit_id} not found")

        # row[0] is id, row[1] is name
        return Unit(
            id=UUID(row[0]),  # Convert string back to UUID
            name=row[1]
        )

    def list_units(self) -> List[Unit]:
        if self.db.cursor is None:
            raise RuntimeError("Database not connected")
        self.db.cursor.execute(
            "SELECT * FROM Unit"
        )
        rows = self.db.cursor.fetchall()  # Gets all rows
        return [
            Unit(
                id=UUID(row[0]),
                name=row[1]
            ) for row in rows
        ]