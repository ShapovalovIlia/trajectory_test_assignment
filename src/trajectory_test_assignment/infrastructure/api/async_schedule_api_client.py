from typing import Dict, Any

import aiohttp

from trajectory_test_assignment.infrastructure.exceptions import (
    ScheduleAPIClientError,
)


class AsyncScheduleAPIClient:
    BASE_URL = "https://ofc-test-01.tspb.su"

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def fetch_schedule_data(self) -> Dict[str, Any]:
        try:
            async with self._session.get(
                f"{self.BASE_URL}/test-task/", ssl=False
            ) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as e:
            raise ScheduleAPIClientError(f"Error fetching data from API {e}")
