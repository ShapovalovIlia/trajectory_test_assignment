from typing import Annotated

from cyclopts import Parameter
from rich import print


async def f(name: Annotated[str, Parameter("--name")]):
    print(f"Hello, {name}!")
