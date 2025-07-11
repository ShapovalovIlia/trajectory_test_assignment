from typing import Dict, Any

import requests


class ScheduleAPIClient:
    BASE_URL = "https://ofc-test-01.tspb.su"

    def __init__(self):
        self._session = requests.Session()

    def fetch_schedule_data(self) -> Dict[str, Any]:
        try:
            response = self._session.get(
                f"{self.BASE_URL}/test-task/", verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка получения данных с API: {e}")
