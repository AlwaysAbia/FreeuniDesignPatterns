import sqlite3
from decimal import Decimal
from typing import Generator
from uuid import uuid4

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.product import Product
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
        unit = Unit(name="kg")
        UnitRepository(init_repository).create_unit(unit)
        return unit

    @pytest.fixture
    def test_unit2(self, init_repository: Database) -> Unit:
        unit = Unit(name="meter")
        UnitRepository(init_repository).create_unit(unit)
        return unit

    def test_product_repository_add_read(
            self, init_repository: Database,test_unit1: Unit, test_unit2: Unit) -> None:
        pr: ProductRepository = ProductRepository(init_repository)

        test_product1 : Product = Product(unit_id=test_unit1.id, name = "apple",
                                          barcode="123123", price=Decimal("3.99"))
        test_product2 : Product = Product(unit_id=test_unit2.id, name = "rope",
                                          barcode="321321", price=Decimal("1.99"))


        pr.create_product(test_product1)
        pr.create_product(test_product2)

        assert(pr.read_product(test_product1.id) == test_product1)
        assert(pr.read_product(test_product2.id) == test_product2)

        assert(pr.list_products() == [test_product1, test_product2])

    def test_product_repository_update_price(
            self, init_repository: Database, test_unit1: Unit) -> None:
        pr = ProductRepository(init_repository)

        test_product = Product(unit_id=test_unit1.id, name="apple",
                               barcode="123123", price=Decimal("3.99"))
        pr.create_product(test_product)

        # Test updating price
        new_price = Decimal("4.99")
        pr.update_product(test_product, new_price)

        updated_product = pr.read_product(test_product.id)
        assert updated_product.price == new_price
        assert updated_product.name == test_product.name

    def test_product_repository_nonexistent_read(
            self, init_repository: Database) -> None:
        pr = ProductRepository(init_repository)
        nonexistent_id = uuid4()

        with pytest.raises(ValueError,
                           match=f"Product with id {nonexistent_id} not found"):
            pr.read_product(nonexistent_id)

    def test_product_repository_duplicate_barcode(
            self, init_repository: Database, test_unit1: Unit) -> None:
        pr = ProductRepository(init_repository)

        product1 = Product(name="apple", unit_id=test_unit1.id,
                           barcode="123123", price=Decimal("3.99"))
        product2 = Product(name="orange", unit_id=test_unit1.id,
                           barcode="123123", price=Decimal("2.99"))  # Same barcode

        pr.create_product(product1)

        with pytest.raises(sqlite3.IntegrityError):  # Assuming barcode is unique
            pr.create_product(product2)

    def test_product_repository_invalid_unit_id(
            self, init_repository: Database) -> None:
        pr = ProductRepository(init_repository)

        # Try to create product with non-existent unit_id
        invalid_product = Product(name="apple", unit_id=uuid4(),
                                  barcode="123123", price=Decimal("3.99"))

        with pytest.raises(sqlite3.IntegrityError):  # Assuming foreign key constraint
            pr.create_product(invalid_product)

    def test_product_repository_empty_list(self, init_repository: Database) -> None:
        pr = ProductRepository(init_repository)
        assert len(pr.list_products()) == 0

    def test_product_repository_null_checks(
            self, init_repository: Database, test_unit1: Unit) -> None:
        pr = ProductRepository(init_repository)

        # Test null name
        with pytest.raises(sqlite3.IntegrityError):
            product = Product(name=None, unit_id=test_unit1.id,  # type: ignore
                              barcode="123123", price=Decimal("3.99"))
            pr.create_product(product)

        # Test null barcode
        with pytest.raises(sqlite3.IntegrityError):
            product = Product(name="apple", unit_id=test_unit1.id,
                              barcode=None, price=Decimal("3.99"))  # type: ignore
            pr.create_product(product)

    def test_product_repository_disconnected_db(self) -> None:
        db = Database(":memory:")  # Don't connect
        pr = ProductRepository(db)

        test_product = Product(name="apple", unit_id=uuid4(),
                               barcode="123123", price=Decimal("3.99"))

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.create_product(test_product)

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.read_product(uuid4())

        with pytest.raises(RuntimeError, match="Database not connected"):
            pr.list_products()