from typing import Any, TypeVar

from fastapi import Depends
from starlette.requests import HTTPConnection

BoundInterface = TypeVar("BoundInterface", bound=type)


def injected(interface: BoundInterface) -> Any:
    async def inject_into_route(conn: HTTPConnection):
        return conn.app.state.injector.get(interface)

    return Depends(inject_into_route)
