import sqlite3
from typing import Generator

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.unit import Unit


#Covers everything except some error handling lines
class TestUnitRepository:
    @pytest.fixture
    def init_repository(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

    def test_unit_repository_add_read(self, init_repository: Database) -> None:
        ur: UnitRepository = UnitRepository(init_repository)

        test_unit1 : Unit = Unit(name = "kg")
        test_unit2 : Unit = Unit(name = "s")
        test_unit3 : Unit = Unit(name = "m")

        ur.create_unit(test_unit1)
        ur.create_unit(test_unit2)
        ur.create_unit(test_unit3)

        assert(ur.read_unit(test_unit1) == test_unit1)
        assert(ur.read_unit(test_unit2) == test_unit2)
        assert(ur.read_unit(test_unit3) == test_unit3)

        assert(ur.list_units() == [test_unit1, test_unit2, test_unit3])

    def test_read_nonexistent_unit(self, init_repository: Database) -> None:
        ur: UnitRepository = UnitRepository(init_repository)
        nonexistent_unit = Unit(name="nonexistent")

        with pytest.raises(ValueError):
            ur.read_unit(nonexistent_unit)

    def test_create_duplicate_unit_name(self, init_repository: Database) -> None:
        ur: UnitRepository = UnitRepository(init_repository)
        unit1 = Unit(name="kg")
        unit2 = Unit(name="kg")  # Same name

        ur.create_unit(unit1)
        with pytest.raises(sqlite3.IntegrityError):
            ur.create_unit(unit2)

    def test_list_empty_repository(self, init_repository: Database) -> None:
        ur: UnitRepository = UnitRepository(init_repository)
        assert ur.list_units() == []