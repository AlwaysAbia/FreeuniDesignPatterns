# db_dependency.py
from typing import Optional

from DPAssignment2.src.db.database import Database


class DatabaseManager:
    _instance : Optional[Database] = None

    @classmethod
    def get_instance(cls) -> Database:
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

def get_db() -> Database:
    return DatabaseManager.get_instance()