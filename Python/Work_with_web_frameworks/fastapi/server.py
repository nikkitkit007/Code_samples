import logging
import asyncio
import uvicorn
from fastapi import FastAPI, Request, APIRouter
from starlette.responses import RedirectResponse
from api.db import migrate, async_session
from api.context import set_session
from server.routes import emotions


app = FastAPI()


@app.on_event("startup")
async def startup():
    # migrate()
    logging.info("start")


@app.on_event("shutdown")
async def shutdown():
    pass


healthcheck_router = APIRouter()
API_PREFIX = "/api"

@healthcheck_router.get('/test')
async def healthcheck():
    return "OK"


def short_module_name(name):
    return name.split('.')[-1]


def module_url(name):
    return f'/{short_module_name(name)}'



def create_routes(app: FastAPI, *modules):
    for m in modules:
        app.include_router(getattr(m, 'r'), prefix=API_PREFIX, tags=[short_module_name(m.__name__)])
    app.include_router(healthcheck_router, tags=["healthcheck"])


create_routes(app, emotions)



def run():
    logging.info(f"Settings: {settings.model_dump()}")
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)


if __name__ == '__main__':
    run()
