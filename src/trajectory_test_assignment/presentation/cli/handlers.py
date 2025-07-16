import traceback
from datetime import date, time
from typing import Annotated

from aiohttp import ClientSession
from rich import print
from cyclopts import Parameter, Token


from trajectory_test_assignment.app import ScheduleDateNotFoundError
from trajectory_test_assignment.infrastructure import (
    AsyncScheduleAPIClient,
    dict_to_schedule,
)


def _str_to_date(_, tokens: list[Token]) -> date:
    return date.fromisoformat(tokens[0].value)


def _str_to_time(_, tokens: list[Token]) -> time:
    return time.fromisoformat(tokens[0].value)


async def get_busy_slots(
    date: Annotated[date, Parameter("--date", converter=_str_to_date)],
) -> None:
    async with ClientSession() as session:
        async_scheduale_api_client = AsyncScheduleAPIClient(session)
        data = await async_scheduale_api_client.fetch_schedule_data()
        schedule = dict_to_schedule(data)

        try:
            busy_slots = schedule.get_busy_slots(date)
        except ScheduleDateNotFoundError as e:
            print(f"[red]Error:[/red] {e}")
            return

        busy_slots.sort()

        for slot in busy_slots:
            print(f"Busy slot: {slot[0]} - {slot[1]} on {date.isoformat()}")


async def get_free_slots(
    date: Annotated[date, Parameter("--date", converter=_str_to_date)],
) -> None:
    async with ClientSession() as session:
        async_scheduale_api_client = AsyncScheduleAPIClient(session)
        data = await async_scheduale_api_client.fetch_schedule_data()

        schedule = dict_to_schedule(data)

        try:
            free_slots = schedule.get_free_slots(date)
        except ScheduleDateNotFoundError as e:
            print(f"[red]Error:[/red] {e}")
            return

        free_slots.sort()
        for slot in free_slots:
            print(f"Free slots: {slot[0]} - {slot[1]} on {date.isoformat()}")


async def is_time_available(
    date: Annotated[date, Parameter("--date", converter=_str_to_date)],
    start_time: Annotated[
        time, Parameter("--start-time", converter=_str_to_time)
    ],
    end_time: Annotated[time, Parameter("--end-time", converter=_str_to_time)],
) -> None:
    async with ClientSession() as session:
        async_scheduale_api_client = AsyncScheduleAPIClient(session)
        data = await async_scheduale_api_client.fetch_schedule_data()

        schedule = dict_to_schedule(data)

        try:
            is_time_available = schedule.is_time_available(
                date, start_time, end_time
            )
        except ScheduleDateNotFoundError as e:
            print(f"[red]Error:[/red] {e}")
            return

        if is_time_available:
            print("The specified time slot is available.")
        else:
            print("The specified time slot is not available.")
