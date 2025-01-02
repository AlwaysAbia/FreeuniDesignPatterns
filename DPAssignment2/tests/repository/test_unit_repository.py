import sqlite3
from typing import Generator

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.unit_repository import UnitRepository


class TestUnitRepository:
    @pytest.fixture
    def init_repository(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

    @pytest.fixture
    def unit_repo(self, init_repository: Database) -> UnitRepository:
        return UnitRepository(init_repository)

    def test_unit_repository_add_read(
            self, unit_repo: UnitRepository
    ) -> None:
        # Create units using the new method
        unit_m = unit_repo.create_unit("m")
        unit_s = unit_repo.create_unit("s")
        unit_kg = unit_repo.create_unit("kg")

        # Read and verify each unit
        assert unit_repo.read_unit(unit_m.id) == unit_m
        assert unit_repo.read_unit(unit_s.id) == unit_s
        assert unit_repo.read_unit(unit_kg.id) == unit_kg

        # Verify list of units
        assert unit_repo.list_units() == [unit_m, unit_s, unit_kg]

    def test_read_nonexistent_unit(
            self, unit_repo: UnitRepository
    ) -> None:
        # Use a UUID that definitely won't exist
        from uuid import uuid4
        nonexistent_id = uuid4()

        assert unit_repo.read_unit(nonexistent_id) is None

    def test_create_duplicate_unit_name(
            self, unit_repo: UnitRepository
    ) -> None:
        # First creation should work fine
        unit_repo.create_unit("kg")

        with pytest.raises(sqlite3.IntegrityError):
            unit_repo.create_unit("kg")

    def test_list_empty_repository(
            self, unit_repo: UnitRepository
    ) -> None:
        assert unit_repo.list_units() == []