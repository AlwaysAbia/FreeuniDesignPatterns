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

    @pytest.fixture
    def unit_kg(self) -> Unit:
        return Unit(name="kg")

    @pytest.fixture
    def unit_s(self) -> Unit:
        return Unit(name="s")

    @pytest.fixture
    def unit_m(self) -> Unit:
        return Unit(name="m")

    @pytest.fixture
    def nonexistent_unit(self) -> Unit:
        return Unit(name="nonexistent")

    def test_unit_repository_add_read(
            self, init_repository: Database,
            unit_m: Unit, unit_s: Unit, unit_kg: Unit) -> None:
        ur: UnitRepository = UnitRepository(init_repository)

        ur.create_unit(unit_m)
        ur.create_unit(unit_s)
        ur.create_unit(unit_kg)

        assert(ur.read_unit(unit_m.id) == unit_m)
        assert(ur.read_unit(unit_s.id) == unit_s)
        assert(ur.read_unit(unit_kg.id) == unit_kg)

        assert(ur.list_units() == [unit_m, unit_s, unit_kg])

    def test_read_nonexistent_unit(
            self, init_repository: Database, nonexistent_unit: Unit) -> None:
        ur: UnitRepository = UnitRepository(init_repository)

        with pytest.raises(ValueError):
            ur.read_unit(nonexistent_unit.id)

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