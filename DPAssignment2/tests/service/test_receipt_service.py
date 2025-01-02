from decimal import Decimal
from typing import Generator, Optional

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.db.service.product_service import ProductService
from DPAssignment2.src.db.service.receipt_service import ReceiptService
from DPAssignment2.src.db.service.unit_service import UnitService
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import Receipt
from DPAssignment2.src.models.unit import Unit


class TestReceiptService:
    @pytest.fixture
    def init_db(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

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
            "test_product1", test_unit1.id,"123213", Decimal("1.25"))

    @pytest.fixture
    def test_product2(self, product_service: ProductService,
                      test_unit2: Unit) -> Product:
        return product_service.create_product(
            "test_product2", test_unit2.id, "321321", Decimal("5.3"))

    def test_create_receipt(self, receipt_service: ReceiptService) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        assert receipt.status
        assert receipt.total == 0
        assert receipt.products == []

    def test_read_by_id_receipt(self, receipt_service: ReceiptService) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        assert receipt == receipt_service.read_by_id_receipt(receipt.id)

    def test_close_receipt(self, receipt_service: ReceiptService) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        assert receipt.status
        receipt_service.close_receipt(receipt.id)
        rec: Optional[Receipt] = receipt_service.read_by_id_receipt(receipt.id)
        if rec is not None:
            assert not rec.status

    def test_delete_receipt(self, receipt_service: ReceiptService) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        receipt_service.delete_receipt(receipt.id)
        assert receipt_service.read_by_id_receipt(receipt.id) is None

    def test_add_product(self, receipt_service: ReceiptService,
                         test_product1: Product, test_product2: Product) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        receipt_service.add_product(receipt.id, test_product1.id, 3)
        receipt_service.add_product(receipt.id, test_product2.id, 6)

        rec: Optional[Receipt] = receipt_service.read_by_id_receipt(receipt.id)
        if rec is not None:
            assert len(rec.products) == 2

    def test_add_to_closed(self, receipt_service: ReceiptService,
                         test_product1: Product) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        receipt_service.close_receipt(receipt.id)
        with pytest.raises(ValueError):
            receipt_service.add_product(receipt.id, test_product1.id, 3)

    def test_add_neg_val(self, receipt_service: ReceiptService,
                         test_product1: Product) -> None:
        receipt: Receipt = receipt_service.create_receipt()
        with pytest.raises(ValueError):
            receipt_service.add_product(receipt.id, test_product1.id, -1)