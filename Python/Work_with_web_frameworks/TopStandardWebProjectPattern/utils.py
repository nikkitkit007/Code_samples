from fastapi import FastAPI, APIRouter
from config import API_PREFIX

healthcheck_router = APIRouter()


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
