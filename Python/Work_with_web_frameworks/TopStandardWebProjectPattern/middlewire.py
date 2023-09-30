from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from context import set_session
from db.connection import async_session


class SessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        async with async_session() as s:
            set_session(s)
            response = await call_next(request)
            await s.commit()
            return response
