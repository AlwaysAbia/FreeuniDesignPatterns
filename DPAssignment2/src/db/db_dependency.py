# db_dependency.py
from DPAssignment2.src.db.database import Database

db = Database()

def get_db() -> Database:
    return db