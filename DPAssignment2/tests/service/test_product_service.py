from decimal import Decimal
from typing import Generator, List, Optional

import pytest

from DPAssignment2.src.db.database import Database
from DPAssignment2.src.db.repository.product_repository import ProductRepository
from DPAssignment2.src.db.repository.unit_repository import UnitRepository
from DPAssignment2.src.db.service.product_service import ProductService
from DPAssignment2.src.db.service.unit_service import UnitService
from DPAssignment2.src.models.product import Product
from DPAssignment2.src.models.unit import Unit


class TestProductService:
    @pytest.fixture
    def init_db(self) -> Generator[Database, None, None]:
        db = Database(":memory:")  # Use in-memory database for testing
        db.connect()
        db.create_tables()
        yield db
        db.disconnect()  # Clean up after test

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

    def test_create_product(self, product_service: ProductService,
                            test_unit1: Unit) -> None:
        prod: Product = product_service.create_product(
            "test_product", test_unit1.id, "123123", Decimal("1.25"))
        assert prod.unit_id == test_unit1.id
        assert prod.name == "test_product"
        assert prod.barcode == "123123"
        assert prod.price == Decimal("1.25")

    def test_read_product(self, product_service: ProductService,
                          test_unit1: Unit) -> None:
        prod: Product = product_service.create_product(
            "test_product", test_unit1.id, "123123", Decimal("1.25"))
        ret = product_service.read_product(prod.id)
        if ret is not None:
            assert product_service.read_product(prod.id) == prod

    def test_list_products(self, product_service: ProductService,
                           test_unit1: Unit, test_unit2: Unit) -> None:
        prod1: Product = product_service.create_product(
            "test_product", test_unit1.id, "123123", Decimal("1.25"))
        prod2: Product = product_service.create_product(
            "test_product2", test_unit2.id, "213213", Decimal("1.5"))
        prods: List[Product] = product_service.list_products()
        assert prod1 in prods
        assert prod2 in prods
        assert len(prods) == 2

    def test_update_product(self, product_service: ProductService,
                            test_unit1: Unit) -> None:
        prod1: Product = product_service.create_product(
            "test_product", test_unit1.id, "123123", Decimal("1.25"))
        prod: Optional[Product] = product_service.read_product(prod1.id)
        if prod is not None:
            assert prod.price == 1.25
            product_service.update_product(prod1.id, Decimal("5"))
            assert prod.price == 5

    def test_bad_create(self, product_service: ProductService,
                        test_unit1: Unit) -> None:
        with pytest.raises(ValueError):
            product_service.create_product(
                "", test_unit1.id, "123123", Decimal("1.25"))
        with pytest.raises(ValueError):
            product_service.create_product(
                "AA", test_unit1.id, "", Decimal("1.25"))
        with pytest.raises(ValueError):
            product_service.create_product(
                "AA", test_unit1.id, "fasf", Decimal("-1.25"))

    def test_bad_update(self, product_service: ProductService,
                        test_unit1: Unit) -> None:
        prod: Product = product_service.create_product(
            "aaaa", test_unit1.id, "123123", Decimal("1.25"))
        with pytest.raises(ValueError):
            product_service.update_product(prod.id, Decimal("-5"))