from decimal import Decimal
from typing import Generator, Optional

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.receipt_repository import ReceiptRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.receipt import Receipt, ReceiptProduct
from DPAssignment2.src.models.unit import Unit


class TestReceiptRepository:
    @pytest.fixture
    def init_repository(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

    @pytest.fixture
    def receipt_repo(self, init_repository: Database) -> ReceiptRepository:
        return ReceiptRepository(init_repository)

    @pytest.fixture
    def product_repo(self, init_repository: Database) -> ProductRepository:
        return ProductRepository(init_repository)

    @pytest.fixture
    def unit_repo(self, init_repository: Database) -> UnitRepository:
        return UnitRepository(init_repository)

    @pytest.fixture
    def sample_unit(self, unit_repo: UnitRepository) -> Unit:
        unit: Unit = unit_repo.create_unit("Sample Unit")
        return unit

    @pytest.fixture
    def sample_product(self, product_repo: ProductRepository,
                       sample_unit: Unit) -> Product:
        product: Product = product_repo.create_product(
            name="Sample Product", price=Decimal("10.00"),
            unit_id=sample_unit.id, barcode="123123")
        return product

    def test_new_product_open(self, receipt_repo: ReceiptRepository) -> None:
        receipt: Receipt = receipt_repo.open_receipt()
        assert receipt.status is True

    def test_close(self, receipt_repo: ReceiptRepository) -> None:
        receipt: Receipt = receipt_repo.open_receipt()
        receipt_repo.close_receipt(receipt.id)
        rec: Optional[Receipt] = receipt_repo.get_receipt(receipt.id)
        if rec is not None:
            assert rec.status is False

    def test_empty_total(self, receipt_repo: ReceiptRepository) -> None:
        receipt: Receipt = receipt_repo.open_receipt()
        assert receipt_repo.get_total(receipt.id) == Decimal(0)

    def test_get_empty_receipt(self, receipt_repo: ReceiptRepository) -> None:
        receipt: Receipt = receipt_repo.open_receipt()
        assert receipt_repo.get_receipt(receipt.id) == receipt

    def test_add_product_to_open_receipt(self, receipt_repo: ReceiptRepository,
                                         sample_product: Product) -> None:
        receipt = receipt_repo.open_receipt()
        receipt_repo.add_product(receipt.id, sample_product.id, 2)
        receipt_with_product = receipt_repo.get_receipt(receipt.id)
        receipt.products.append(ReceiptProduct(product_id=sample_product.id,
                                               quantity=2,
                                               price_when_sold=sample_product.price))

        assert receipt == receipt_with_product
        assert len(receipt_with_product.products) == 1
        assert receipt_with_product.products[0].product_id == sample_product.id
        assert receipt_with_product.products[0].quantity == 2
        assert receipt_with_product.products[0].price_when_sold == sample_product.price

    def test_receipt_total_update(self, receipt_repo: ReceiptRepository,
                                  sample_product: Product) -> None:
        receipt = receipt_repo.open_receipt()
        total = receipt_repo.get_total(receipt.id)
        assert total == Decimal("0")
        receipt_repo.add_product(receipt.id, sample_product.id, 3)
        total = receipt_repo.get_total(receipt.id)
        assert total == Decimal("30.00")  # 3 * 10.00

    def test_add_duplicate_product(self, receipt_repo: ReceiptRepository,
                                   sample_product: Product) -> None:
        receipt = receipt_repo.open_receipt()
        receipt_repo.add_product(receipt.id, sample_product.id, 2)
        receipt_repo.add_product(receipt.id, sample_product.id, 3)
        receipt_with_product: Optional[Receipt] = receipt_repo.get_receipt(receipt.id)

        if receipt_with_product is not None:
            assert len(receipt_with_product.products) == 1
            assert receipt_with_product.products[0].quantity == 5  # 2 + 3
            assert (receipt_with_product.products[0].price_when_sold
                    == sample_product.price)


    def test_delete_receipt(self, receipt_repo: ReceiptRepository,
                            sample_product: Product) -> None:
        receipt = receipt_repo.open_receipt()
        receipt_repo.add_product(receipt.id, sample_product.id, 2)

        receipt_repo.delete_receipt(receipt.id)
        assert receipt_repo.get_receipt(receipt.id) is None