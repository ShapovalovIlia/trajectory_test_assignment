import pytest
import aiohttp

from trajectory_test_assignment.infrastructure.api.async_schedule_api_client import (
    AsyncScheduleAPIClient,
)
from trajectory_test_assignment.infrastructure.exceptions import (
    ScheduleAPIClientError,
)


@pytest.mark.asyncio
async def test_fetch_schedule_data_real():
    async with aiohttp.ClientSession() as session:
        client = AsyncScheduleAPIClient(session)
        data = await client.fetch_schedule_data()
        assert isinstance(data, dict)
        assert "days" in data or "timeslots" in data


@pytest.mark.asyncio
async def test_fetch_schedule_data_real_fail():
    async with aiohttp.ClientSession() as session:
        client = AsyncScheduleAPIClient(session)
        client.BASE_URL = "https://nonexistent-url-for-test.tspb.su"
        with pytest.raises(ScheduleAPIClientError):
            await client.fetch_schedule_data()
