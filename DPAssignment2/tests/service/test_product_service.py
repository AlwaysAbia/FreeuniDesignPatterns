from typing import Generator

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.service.product_service import ProductService


class TestUnitService:
    @pytest.fixture
    def product_service(self) -> Generator[ProductService, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield ProductService(ProductRepository(db))
        db.disconnect()

