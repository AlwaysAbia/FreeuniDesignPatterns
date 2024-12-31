from decimal import Decimal
from typing import Generator

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.db.repository.sales_repository import SalesRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import Receipt
from DPAssignment2.src.models.unit import Unit


class TestSalesRepository():
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

    @pytest.fixture
    def product_repo(self, init_repository: Database) -> ProductRepository:
        return ProductRepository(init_repository)

    @pytest.fixture
    def receipt_repo(self, init_repository: Database) -> ReceiptRepository:
        return ReceiptRepository(init_repository)

    @pytest.fixture
    def sales_repo(self, init_repository: Database) -> SalesRepository:
        return SalesRepository(init_repository)

    @pytest.fixture
    def sample_unit(self, unit_repo: UnitRepository) -> Unit:
        unit: Unit = unit_repo.create_unit("Sample Unit")
        return unit

    @pytest.fixture
    def sample_product1(self, product_repo: ProductRepository,
                       sample_unit: Unit) -> Product:
        product: Product = product_repo.create_product(
            name="Sample Product1", price=Decimal("10.00"),
            unit_id=sample_unit.id, barcode="123123")
        return product

    @pytest.fixture
    def sample_product2(self, product_repo: ProductRepository,
                        sample_unit: Unit) -> Product:
        product: Product = product_repo.create_product(
            name="Sample Product2", price=Decimal("15.00"),
            unit_id=sample_unit.id, barcode="211211")
        return product

    def test_no_sales(self, sales_repo: SalesRepository):
        assert sales_repo.get_n_receipts() == 0
        assert sales_repo.get_revenue() == 0

    def test_sales(self, sales_repo: SalesRepository, receipt_repo: ReceiptRepository,
                       sample_product1: Product, sample_product2: Product):
        receipt: Receipt = receipt_repo.open_receipt()
        receipt_repo.add_product(receipt.id, sample_product1.id, 5)
        receipt_repo.add_product(receipt.id, sample_product2.id, 10)
        receipt_repo.close_receipt(receipt.id)
        assert sales_repo.get_n_receipts() == 1
        assert sales_repo.get_revenue() == 5*10+10*15
        receipt_repo.delete_receipt(receipt.id)
        assert sales_repo.get_n_receipts() == 0
        assert sales_repo.get_revenue() == 0


