from decimal import Decimal
from typing import Generator
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from DPAssignment2.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def mock_service() -> Generator[Mock, None, None]:
    with patch('DPAssignment2.src.api.sales_api.SalesService') as MockService:
        mock = Mock()
        MockService.return_value = mock
        yield mock

class TestGetSalesReport:
    def test_get_sales_report_success(self, test_client: TestClient,
                                      mock_service: Mock) -> None:
        # Setup
        mock_service.get_n_receipts.return_value = 23
        mock_service.get_revenue.return_value = Decimal("456890")

        # Execute
        response = test_client.get("/sales")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "sales": {
                "n_receipts": 23,
                "revenue": "456890"
            }
        }
        mock_service.get_n_receipts.assert_called_once()
        mock_service.get_revenue.assert_called_once()