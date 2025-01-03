from typing import Generator
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from DPAssignment2.main import app

# Constants
SAMPLE_UNIT_ID = UUID('27b4f218-1cc2-4694-b131-ad481dc08901')
SAMPLE_UNIT_2_ID = UUID('ddcce001-a295-4d5f-b016-1de552a7f324')

# Test data
SAMPLE_UNIT = {
    "id": str(SAMPLE_UNIT_ID),
    "name": "კგ"
}

SAMPLE_UNIT_2 = {
    "id": str(SAMPLE_UNIT_2_ID),
    "name": "ცალი"
}

# Fixtures
@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def mock_service() -> Generator[Mock, None, None]:
    with patch('DPAssignment2.src.api.unit_api.UnitService') as MockService:
        mock = Mock()
        MockService.return_value = mock
        yield mock

# Tests for POST /units
class TestCreateUnit:
    def test_create_unit_success(self, test_client: TestClient,
                                 mock_service: Mock) -> None:
        # Setup
        mock_service.create_unit.return_value.id = SAMPLE_UNIT_ID
        mock_service.create_unit.return_value.name = "კგ"

        # Execute
        response = test_client.post("/units", json={"name": "კგ"})

        # Assert
        assert response.status_code == 201
        assert response.json() == {"unit": SAMPLE_UNIT}
        mock_service.create_unit.assert_called_once_with("კგ")

    def test_create_unit_conflict(self, test_client: TestClient,
                                  mock_service: Mock) -> None:
        # Setup
        mock_service.create_unit.side_effect = (
            ValueError("Unit with name<კგ> already exists."))

        # Execute
        response = test_client.post("/units", json={"name": "კგ"})

        # Assert
        assert response.status_code == 409
        assert response.json() == {
            "detail": {"message": "Unit with name<კგ> already exists."}
        }

    def test_create_unit_empty_name(self, test_client: TestClient,
                                    mock_service: Mock) -> None:
        # Setup
        mock_service.create_unit.side_effect = (
            ValueError("Can't create unit with no name"))

        # Execute
        response = test_client.post("/units", json={"name": ""})

        # Assert
        assert response.status_code == 409
        assert response.json() == {
            "detail": {"message": "Can't create unit with no name"}
        }

    def test_create_unit_missing_name(self, test_client: TestClient) -> None:
        # Execute
        response = test_client.post("/units", json={})

        # Assert
        assert response.status_code == 422  # FastAPI validation error

# Tests for GET /units/{unit_id}
class TestGetUnit:
    def test_get_unit_success(self, test_client: TestClient,
                              mock_service: Mock) -> None:
        # Setup
        mock_service.read_unit.return_value.id = SAMPLE_UNIT_ID
        mock_service.read_unit.return_value.name = "კგ"

        # Execute
        response = test_client.get(f"/units/{SAMPLE_UNIT_ID}")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"unit": SAMPLE_UNIT}
        mock_service.read_unit.assert_called_once_with(SAMPLE_UNIT_ID)

    def test_get_unit_not_found(self, test_client: TestClient,
                                mock_service: Mock) -> None:
        # Setup
        mock_service.read_unit.return_value = None

        # Execute
        response = test_client.get(f"/units/{SAMPLE_UNIT_ID}")

        # Assert
        assert response.status_code == 404
        assert response.json() == {
            "detail": {"message": f"Unit with id<{SAMPLE_UNIT_ID}> does not exist."}
        }

    def test_get_unit_invalid_uuid(self, test_client: TestClient) -> None:
        # Execute
        response = test_client.get("/units/not-a-uuid")

        # Assert
        assert response.status_code == 422  # FastAPI validation error

# Tests for GET /units
class TestListUnits:
    def test_list_units_success(self, test_client: TestClient,
                                mock_service: Mock) -> None:
        # Setup
        mock_unit1 = Mock()
        mock_unit1.id = SAMPLE_UNIT_ID
        mock_unit1.name = "კგ"  # Set as string directly

        mock_unit2 = Mock()
        mock_unit2.id = SAMPLE_UNIT_2_ID
        mock_unit2.name = "ცალი"  # Set as string directly

        mock_service.list_units.return_value = [mock_unit1, mock_unit2]

        # Execute
        response = test_client.get("/units")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            "units": [SAMPLE_UNIT, SAMPLE_UNIT_2]
        }

    def test_list_units_empty(self, test_client: TestClient,
                              mock_service: Mock) -> None:
        # Setup
        mock_service.list_units.return_value = []

        # Execute
        response = test_client.get("/units")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"units": []}