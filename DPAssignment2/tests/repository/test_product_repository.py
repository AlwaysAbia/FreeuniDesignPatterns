import sqlite3
from decimal import Decimal
from typing import Generator
from uuid import uuid4

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.unit import Unit


class TestProductRepository:
    @pytest.fixture
    def init_repository(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

    @pytest.fixture
    def test_unit1(self, init_repository: Database) -> Unit:
        return UnitRepository(init_repository).create_unit("kg")

    @pytest.fixture
    def test_unit2(self, init_repository: Database) -> Unit:
        return UnitRepository(init_repository).create_unit("meter")

    @pytest.fixture
    def product_repo(self, init_repository: Database) -> ProductRepository:
        return ProductRepository(init_repository)

    def test_product_repository_add_read(
            self,
            product_repo: ProductRepository,
            test_unit1: Unit,
            test_unit2: Unit
    ) -> None:
        # Create products using the new method
        test_product1 = product_repo.create_product(
            name="apple",
            unit_id=test_unit1.id,
            barcode="123123",
            price=Decimal("3.99")
        )
        test_product2 = product_repo.create_product(
            name="rope",
            unit_id=test_unit2.id,
            barcode="321321",
            price=Decimal("1.99")
        )

        # Read and verify each product
        assert product_repo.read_product(test_product1.id) == test_product1
        assert product_repo.read_product(test_product2.id) == test_product2
        assert product_repo.list_products() == [test_product1, test_product2]

    def test_product_repository_update_price(
            self,
            product_repo: ProductRepository,
            test_unit1: Unit
    ) -> None:
        # Create a product first
        test_product1 = product_repo.create_product(
            name="apple",
            unit_id=test_unit1.id,
            barcode="123123",
            price=Decimal("3.99")
        )

        # Test updating price
        new_price = Decimal("4.99")
        product_repo.update_product(test_product1, new_price)

        updated_product = product_repo.read_product(test_product1.id)
        assert updated_product.price == new_price
        assert updated_product.name == test_product1.name

    def test_product_repository_nonexistent_read(
            self, product_repo: ProductRepository
    ) -> None:
        nonexistent_id = uuid4()

        with pytest.raises(ValueError,
                           match=f"Product with id {nonexistent_id} not found"):
            product_repo.read_product(nonexistent_id)

    def test_product_repository_duplicate_barcode(
            self,
            product_repo: ProductRepository,
            test_unit1: Unit
    ) -> None:
        # First product creation should work fine
        product_repo.create_product(
            name="apple",
            unit_id=test_unit1.id,
            barcode="123123",
            price=Decimal("3.99")
        )

        with pytest.raises(sqlite3.IntegrityError):
            product_repo.create_product(
                name="orange",
                unit_id=test_unit1.id,
                barcode="123123",
                price=Decimal("2.99")
            )

    def test_product_repository_invalid_unit_id(
            self, product_repo: ProductRepository
    ) -> None:
        # Try to create product with non-existent unit_id
        with pytest.raises(sqlite3.IntegrityError):  # Assuming foreign key constraint
            product_repo.create_product(
                name="apple",
                unit_id=uuid4(),
                barcode="123123",
                price=Decimal("3.99")
            )

    def test_product_repository_empty_list(
            self, product_repo: ProductRepository
    ) -> None:
        assert len(product_repo.list_products()) == 0

    def test_product_repository_null_checks(
            self,
            product_repo: ProductRepository,
            test_unit1: Unit
    ) -> None:
        # Test null name
        with pytest.raises(sqlite3.IntegrityError):
            product_repo.create_product(
                name=None,  # type: ignore
                unit_id=test_unit1.id,
                barcode="123123",
                price=Decimal("3.99")
            )

        # Test null barcode
        with pytest.raises(sqlite3.IntegrityError):
            product_repo.create_product(
                name="apple",
                unit_id=test_unit1.id,
                barcode=None,  # type: ignore
                price=Decimal("3.99")
            )

    def test_product_repository_disconnected_db(self) -> None:
        db = Database(":memory:")  # Don't connect
        pr = ProductRepository(db)

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.create_product(
                name="apple",
                unit_id=uuid4(),
                barcode="123123",
                price=Decimal("3.99")
            )

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.read_product(uuid4())

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.list_products()