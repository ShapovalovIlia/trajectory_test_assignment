from typing import Dict, Any

import aiohttp


class AsyncScheduleAPIClient:
    BASE_URL = "https://ofc-test-01.tspb.su"

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def fetch_schedule_data(self) -> Dict[str, Any]:
        if not self._session:
            raise RuntimeError(
                "Session not initialized. Use within 'async with'."
            )

        try:
            async with self._session.get(
                f"{self.BASE_URL}/test-task/", ssl=False
            ) as response:
                response.raise_for_status()

                return await response.json()

        except aiohttp.ClientError as e:
            raise RuntimeError(f"Ошибка получения данных с API: {e}")
