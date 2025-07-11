import pytest

from trajectory_test_assignment.infrastructure import AsyncScheduleAPIClient


@pytest.fixture
def mock_response():
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


url = "https://ofc-test-01.tspb.su/test-task/"


@pytest.mark.asyncio
async def test_fetch_schedule_data_success(mock_response):
    async with AsyncScheduleAPIClient() as client:
        data = await client.fetch_schedule_data()
        assert data == mock_response


@pytest.mark.asyncio
async def test_fetch_schedule_data_http_error():
    async with AsyncScheduleAPIClient() as client:
        client.BASE_URL = "123"

        with pytest.raises(RuntimeError):
            await client.fetch_schedule_data()


@pytest.mark.asyncio
async def test_fetch_without_context_raises():
    client = AsyncScheduleAPIClient()

    with pytest.raises(RuntimeError):
        await client.fetch_schedule_data()


@pytest.mark.asyncio
async def test_session_closed_after_context(mock_response):
    client = AsyncScheduleAPIClient()
    async with client:
        data = await client.fetch_schedule_data()

    assert client._session.closed  # noqa: SLF001 type: ignore


@pytest.mark.asyncio
async def test_multiple_fetches_in_context(mock_response):
    async with AsyncScheduleAPIClient() as client:
        data1 = await client.fetch_schedule_data()
        data2 = await client.fetch_schedule_data()

        assert data1 == mock_response
        assert data2 == mock_response
