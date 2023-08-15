from fastapi import FastAPI
from injector import Injector

from news_toolkit_api.api.v1.middlewares import CacheControlMiddleware
from news_toolkit_api.api.v1.routers import router


def create_app(injector: Injector) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.state.injector = injector
    app.add_middleware(CacheControlMiddleware)
    return app
