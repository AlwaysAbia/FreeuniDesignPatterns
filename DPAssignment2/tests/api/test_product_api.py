from decimal import Decimal
from typing import Generator
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from DPAssignment2.main import app

# Constants
SAMPLE_PRODUCT_ID = UUID('7d3184ae-80cd-417f-8b14-e3de42a98031')
SAMPLE_UNIT_ID = UUID('27b4f218-1cc2-4694-b131-ad481dc08901')

# Test data
SAMPLE_PRODUCT = {
    "id": str(SAMPLE_PRODUCT_ID),
    "unit_id": str(SAMPLE_UNIT_ID),
    "name": "Apple",
    "barcode": "1234567890",
    "price": "520.00"
}

# Fixtures
@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def mock_service() -> Generator[Mock, None, None]:
    with patch('DPAssignment2.src.api.product_api.ProductService') as MockService:
        mock = Mock()
        MockService.return_value = mock
        yield mock

# Tests for POST /products
class TestCreateProduct:
    def test_create_product_success(self, test_client: TestClient,
                                    mock_service: Mock) -> None:
        # Setup
        mock_service.create_product.return_value.id = SAMPLE_PRODUCT_ID
        mock_service.create_product.return_value.unit_id = SAMPLE_UNIT_ID
        mock_service.create_product.return_value.name = "Apple"
        mock_service.create_product.return_value.barcode = "1234567890"
        mock_service.create_product.return_value.price = Decimal("520.00")

        # Execute
        response = test_client.post("/products", json={
            "unit_id": str(SAMPLE_UNIT_ID),
            "name": "Apple",
            "barcode": "1234567890",
            "price": "520.00"
        })

        # Assert
        assert response.status_code == 201
        assert response.json() == {"product": SAMPLE_PRODUCT}
        mock_service.create_product.assert_called_once_with(
            name="Apple",
            unit_id=SAMPLE_UNIT_ID,
            barcode="1234567890",
            price=Decimal("520.00")
        )

    def test_create_product_duplicate_barcode(self, test_client: TestClient,
                                              mock_service: Mock) -> None:
        # Setup
        mock_service.create_product.side_effect = (
            ValueError("Product with barcode<1234567890> already exists."))

        # Execute
        response = test_client.post("/products", json={
            "unit_id": str(SAMPLE_UNIT_ID),
            "name": "Apple",
            "barcode": "1234567890",
            "price": "520.00"
        })

        # Assert
        assert response.status_code == 409
        assert response.json() == {
            "detail": {"message": "Product with barcode<1234567890> already exists."}
        }

# Tests for GET /products/{product_id}
class TestGetProduct:
    def test_get_product_success(self, test_client: TestClient,
                                 mock_service: Mock) -> None:
        # Setup
        mock_service.read_product.return_value.id = SAMPLE_PRODUCT_ID
        mock_service.read_product.return_value.unit_id = SAMPLE_UNIT_ID
        mock_service.read_product.return_value.name = "Apple"
        mock_service.read_product.return_value.barcode = "1234567890"
        mock_service.read_product.return_value.price = Decimal("520.00")

        # Execute
        response = test_client.get(f"/products/{SAMPLE_PRODUCT_ID}")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"product": SAMPLE_PRODUCT}
        mock_service.read_product.assert_called_once_with(SAMPLE_PRODUCT_ID)

    def test_get_product_not_found(self, test_client: TestClient,
                                   mock_service: Mock) -> None:
        # Setup
        mock_service.read_product.return_value = None

        # Execute
        response = test_client.get(f"/products/{SAMPLE_PRODUCT_ID}")

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": {"message":
                           f"Product with id<{SAMPLE_PRODUCT_ID}> does not exist."}
        }

# Tests for GET /products
class TestListProducts:
    def test_list_products_success(self, test_client: TestClient,
                                   mock_service: Mock) -> None:
        # Setup
        mock_product = Mock()
        mock_product.id = SAMPLE_PRODUCT_ID
        mock_product.unit_id = SAMPLE_UNIT_ID
        mock_product.name = "Apple"
        mock_product.barcode = "1234567890"
        mock_product.price = Decimal("520.00")

        mock_service.list_products.return_value = [mock_product]

        # Execute
        response = test_client.get("/products")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "products": [SAMPLE_PRODUCT]
        }

# Tests for PATCH /products/{product_id}
class TestUpdateProduct:
    def test_update_product_success(self, test_client: TestClient,
                                    mock_service: Mock) -> None:
        # Execute
        response = test_client.patch(
            f"/products/{SAMPLE_PRODUCT_ID}",
            json={"price": "530.00"}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {}
        mock_service.update_product.assert_called_once_with(
            SAMPLE_PRODUCT_ID,
            Decimal("530.00")
        )

    def test_update_product_not_found(self, test_client: TestClient,
                                      mock_service: Mock) -> None:
        # Setup
        mock_service.update_product.side_effect = ValueError(
            f"Product with id<{SAMPLE_PRODUCT_ID}> does not exist."
        )

        # Execute
        response = test_client.patch(
            f"/products/{SAMPLE_PRODUCT_ID}",
            json={"price": "530.00"}
        )

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": {"message":
                           f"Product with id<{SAMPLE_PRODUCT_ID}> does not exist."}
        }