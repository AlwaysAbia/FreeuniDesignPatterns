import sqlite3
from abc import ABC, abstractmethod
from typing import Any, List
from uuid import UUID, uuid4

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.models.unit import Unit


class IUnitRepository(ABC):
    @abstractmethod
    def create_unit(self, unit_name: str) -> Unit:
        pass

    @abstractmethod
    def read_unit(self, unit_id: UUID) -> Unit:
        pass

    @abstractmethod
    def list_units(self) -> List[Unit]:
        pass

class UnitRepository(IUnitRepository):
   def __init__(self, database: Database) -> None:
       self.db = database

   def _execute_query(self, query: str, params: tuple[Any, ...]) -> None:
       if self.db.cursor is None:
           raise RuntimeError("Database not connected")
       self.db.cursor.execute(query, params)

   def create_unit(self, unit_name: str) -> Unit:
       unit_id = uuid4()
       try:
           self._execute_query(
               "INSERT INTO Unit (id, name) VALUES (?, ?)",
               (str(unit_id), unit_name)
           )
           self.db.commit()
           return Unit(id=unit_id, name=unit_name)
       except sqlite3.Error as e:
           self.db.rollback()
           raise e

   def read_unit(self, unit_id: UUID) -> Unit:
       self._execute_query("SELECT * FROM Unit WHERE id = ?", (str(unit_id),))
       assert self.db.cursor is not None
       row = self.db.cursor.fetchone()
       if row is None:
           raise ValueError(f"Unit with id {unit_id} not found")
       return Unit(id=UUID(row[0]), name=row[1])

   def list_units(self) -> List[Unit]:
       self._execute_query("SELECT * FROM Unit", ())
       assert self.db.cursor is not None
       return [Unit(id=UUID(row[0]), name=row[1])
               for row in self.db.cursor.fetchall()]