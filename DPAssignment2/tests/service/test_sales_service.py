from decimal import Decimal
from typing import Generator

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.db.repository.sales_repository import SalesRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.db.service.product_service import ProductService
from DPAssignment2.src.db.service.receipt_service import ReceiptService
from DPAssignment2.src.db.service.sales_service import SalesService
from DPAssignment2.src.db.service.unit_service import UnitService
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import Receipt
from DPAssignment2.src.models.unit import Unit


class TestSalesService:
    @pytest.fixture
    def init_db(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

    @pytest.fixture
    def sales_service(self, init_db: Database) -> SalesService:
        return SalesService(SalesRepository(init_db))

    @pytest.fixture
    def receipt_service(self, init_db: Database) -> ReceiptService:
        return ReceiptService(ReceiptRepository(init_db))

    @pytest.fixture
    def product_service(self, init_db: Database) -> ProductService:
        return ProductService(ProductRepository(init_db))

    @pytest.fixture
    def unit_service(self, init_db: Database) -> UnitService:
        return UnitService(UnitRepository(init_db))

    @pytest.fixture
    def test_unit1(self, unit_service: UnitService) -> Unit:
        return unit_service.create_unit("test_unit1")

    @pytest.fixture
    def test_unit2(self, unit_service: UnitService) -> Unit:
        return unit_service.create_unit("test_unit2")

    @pytest.fixture
    def test_product1(self, product_service: ProductService,
                      test_unit1: Unit) -> Product:
        return product_service.create_product(
            "test_product1", test_unit1.id, "123213", Decimal("1.25"))

    @pytest.fixture
    def test_product2(self, product_service: ProductService,
                      test_unit2: Unit) -> Product:
        return product_service.create_product(
            "test_product2", test_unit2.id, "321321", Decimal("5.3"))

    def test_n_receipt(self, sales_service: SalesService,
                       receipt_service: ReceiptService,
                     test_product1: Product, test_product2: Product) -> None:
        receipt_service.create_receipt()

        assert sales_service.get_n_receipts() == 1
        receipt_service.create_receipt()
        assert sales_service.get_n_receipts() == 2

    def test_revenue(self, sales_service: SalesService, receipt_service: ReceiptService,
                     test_product1: Product, test_product2: Product) -> None:
        rec: Receipt = receipt_service.create_receipt()
        receipt_service.add_product(rec.id, test_product1.id, 3)
        receipt_service.add_product(rec.id, test_product2.id, 3)

        assert sales_service.get_revenue() == 3*1.25 + 3*5.3