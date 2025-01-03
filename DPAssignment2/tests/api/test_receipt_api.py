from decimal import Decimal
from typing import Generator
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from DPAssignment2.main import app
from DPAssignment2.src.models.receipt import Receipt, ReceiptProduct

# Constants
SAMPLE_RECEIPT_ID = UUID('25f13441-5fab-4b12-aefe-3fa0089fb63a')
SAMPLE_PRODUCT_ID = UUID('7d3184ae-80cd-417f-8b14-e3de42a98031')

# Fixtures
@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def mock_service() -> Generator[Mock, None, None]:
    with patch('DPAssignment2.src.api.receipt_api.ReceiptService') as MockService:
        mock = Mock()
        MockService.return_value = mock
        yield mock

class TestCreateReceipt:
    def test_create_receipt_success(self, test_client: TestClient,
                                    mock_service: Mock) -> None:
        mock_receipt = Receipt(id=SAMPLE_RECEIPT_ID)
        mock_service.create_receipt.return_value = mock_receipt

        response = test_client.post("/receipts")

        assert response.status_code == 201
        assert response.json() == {
            "receipt": {
                "id": str(SAMPLE_RECEIPT_ID),
                "status": True,
                "products": [],
                "total": "0.00"
            }
        }

class TestAddProduct:
    def test_add_product_success(self, test_client: TestClient,
                                 mock_service: Mock) -> None:
        product = ReceiptProduct(
            product_id=SAMPLE_PRODUCT_ID,
            quantity=123,
            price_when_sold=Decimal("520.00")
        )
        mock_receipt = Receipt(
            id=SAMPLE_RECEIPT_ID,
            products=[product],
            total=Decimal("63960.00")
        )
        mock_service.add_product.return_value = mock_receipt

        response = test_client.post(
            f"/receipts/{SAMPLE_RECEIPT_ID}/products",
            json={"id": str(SAMPLE_PRODUCT_ID), "quantity": 123}
        )

        assert response.status_code == 201
        assert response.json() == {
            "receipt": {
                "id": str(SAMPLE_RECEIPT_ID),
                "status": True,
                "products": [{
                    "product_id": str(SAMPLE_PRODUCT_ID),
                    "quantity": 123,
                    "price_when_sold": "520.00"
                }],
                "total": "63960.00"
            }
        }

    def test_add_product_not_found(self, test_client: TestClient,
                                   mock_service: Mock) -> None:
        mock_service.add_product.side_effect = ValueError("Receipt not found")

        response = test_client.post(
            f"/receipts/{SAMPLE_RECEIPT_ID}/products",
            json={"id": str(SAMPLE_PRODUCT_ID), "quantity": 123}
        )

        assert response.status_code == 404
        assert response.json() == {"detail": {"message": "Receipt not found"}}

class TestGetReceipt:
    def test_get_receipt_success(self, test_client: TestClient,
                                 mock_service: Mock) -> None:
        product = ReceiptProduct(
            product_id=SAMPLE_PRODUCT_ID,
            quantity=123,
            price_when_sold=Decimal("520.00")
        )
        mock_receipt = Receipt(
            id=SAMPLE_RECEIPT_ID,
            products=[product],
            total=Decimal("63960.00")
        )
        mock_service.read_by_id_receipt.return_value = mock_receipt

        response = test_client.get(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 200
        assert response.json() == {
            "receipt": {
                "id": str(SAMPLE_RECEIPT_ID),
                "status": True,
                "products": [{
                    "product_id": str(SAMPLE_PRODUCT_ID),
                    "quantity": 123,
                    "price_when_sold": "520.00"
                }],
                "total": "63960.00"
            }
        }

    def test_get_receipt_not_found(self, test_client: TestClient,
                                   mock_service: Mock) -> None:
        mock_service.read_by_id_receipt.return_value = None

        response = test_client.get(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 404
        assert response.json() == {
            "detail": {"message":
                           f"Receipt with id<{SAMPLE_RECEIPT_ID}> does not exist."}
        }

class TestCloseReceipt:
    def test_close_receipt_success(self, test_client: TestClient,
                                   mock_service: Mock) -> None:
        response = test_client.patch(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 200
        assert response.json() == {}

    def test_close_receipt_not_found(self, test_client: TestClient,
                                     mock_service: Mock) -> None:
        mock_service.close_receipt.side_effect = ValueError("Receipt not found")

        response = test_client.patch(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": {"message": "Receipt not found"}}

class TestDeleteReceipt:
    def test_delete_receipt_success(self, test_client: TestClient,
                                    mock_service: Mock) -> None:
        response = test_client.delete(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 200
        assert response.json() == {}

    def test_delete_receipt_not_found(self, test_client: TestClient,
                                      mock_service: Mock) -> None:
        mock_service.delete_receipt.side_effect = ValueError("Receipt not found")

        response = test_client.delete(f"/receipts/{SAMPLE_RECEIPT_ID}")

        assert response.status_code == 404
        assert response.json() == {"detail": {"message": "Receipt not found"}}