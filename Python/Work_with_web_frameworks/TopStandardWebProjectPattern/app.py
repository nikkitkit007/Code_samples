from config import settings, server_log
import asyncio

import uvicorn
from fastapi import FastAPI
from db.connection import migrate, async_session
from middlewire import SessionMiddleware
from context import set_session
from routes import route1
from utils import create_routes


app = FastAPI()
app.add_middleware(SessionMiddleware)


@app.on_event("startup")
async def startup():
    migrate()
    async with async_session() as session:
        set_session(session)


@app.on_event("shutdown")
async def shutdown():
    pass


create_routes(app, route1)


def run():
    server_log.info(f"Settings: {settings.model_dump()}")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)


if __name__ == '__main__':
    run()
