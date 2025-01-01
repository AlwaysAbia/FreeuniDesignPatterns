from typing import Generator
from uuid import uuid4

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.db.service.unit_service import UnitService


class TestUnitService:
    @pytest.fixture
    def unit_service(self) -> Generator[UnitService, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield UnitService(UnitRepository(db))
        db.disconnect()

    def test_create_unit(self, unit_service: UnitService) -> None:
        unit = unit_service.create_unit("kg")
        assert unit.name == "kg"

    def test_create_unit_empty_name(self, unit_service: UnitService) -> None:
        with pytest.raises(ValueError):
            unit_service.create_unit("")

    def test_read_unit(self, unit_service: UnitService) -> None:
        created = unit_service.create_unit("meter")
        read = unit_service.read_unit(created.id)
        assert read == created

    def test_read_nonexistent_unit(self, unit_service: UnitService) -> None:
        with pytest.raises(ValueError):
            unit_service.read_unit(uuid4())

    def test_list_units(self, unit_service: UnitService) -> None:
        unit1 = unit_service.create_unit("kg")
        unit2 = unit_service.create_unit("meter")
        units = unit_service.list_units()
        assert len(units) == 2
        assert unit1 in units
        assert unit2 in units