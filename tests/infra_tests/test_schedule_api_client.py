import requests
import pytest
from unittest.mock import patch, MagicMock

from trajectory_test_assignment.infrastructure import ScheduleAPIClient


@pytest.fixture
def mock_response_data():
    return {
        "days": [
            {"id": 1, "date": "2025-02-15", "start": "09:00", "end": "21:00"},
            {"id": 2, "date": "2025-02-16", "start": "08:00", "end": "22:00"},
            {"id": 3, "date": "2025-02-17", "start": "09:00", "end": "18:00"},
            {"id": 4, "date": "2025-02-18", "start": "10:00", "end": "18:00"},
            {"id": 5, "date": "2025-02-19", "start": "09:00", "end": "18:00"},
        ],
        "timeslots": [
            {"id": 1, "day_id": 1, "start": "17:30", "end": "20:00"},
            {"id": 2, "day_id": 1, "start": "09:00", "end": "12:00"},
            {"id": 3, "day_id": 2, "start": "14:30", "end": "18:00"},
            {"id": 4, "day_id": 2, "start": "09:30", "end": "11:00"},
            {"id": 5, "day_id": 3, "start": "12:30", "end": "18:00"},
            {"id": 6, "day_id": 4, "start": "10:00", "end": "11:00"},
            {"id": 7, "day_id": 4, "start": "11:30", "end": "14:00"},
            {"id": 8, "day_id": 4, "start": "14:00", "end": "16:00"},
            {"id": 9, "day_id": 4, "start": "17:00", "end": "18:00"},
        ],
    }


@patch(
    "trajectory_test_assignment.infrastructure.schedule_api_client.requests.Session.get"
)
def test_fetch_schedule_data_success(mock_get, mock_response_data):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = ScheduleAPIClient()
    data = client.fetch_schedule_data()
    assert data == mock_response_data


@patch(
    "trajectory_test_assignment.infrastructure.schedule_api_client.requests.Session.get"
)
def test_fetch_schedule_data_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )
    mock_get.return_value = mock_response

    client = ScheduleAPIClient()
    with pytest.raises(RuntimeError):
        client.fetch_schedule_data()


@patch(
    "trajectory_test_assignment.infrastructure.schedule_api_client.requests.Session.get"
)
def test_fetch_schedule_data_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Connection failed"
    )

    client = ScheduleAPIClient()
    with pytest.raises(RuntimeError):
        client.fetch_schedule_data()


def test_session_is_initialized():
    client = ScheduleAPIClient()
    assert client._session is not None  # noqa: SLF001
