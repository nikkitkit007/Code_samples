from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

ctx_session = ContextVar('ctx_session', default=None)


def get_session() -> AsyncSession:
    return ctx_session.get()


def set_session(session: AsyncSession):
    ctx_session.set(session)


def session() -> AsyncSession:
    s = get_session()
    if not s:
        raise Exception('Session is not set')
    return s
