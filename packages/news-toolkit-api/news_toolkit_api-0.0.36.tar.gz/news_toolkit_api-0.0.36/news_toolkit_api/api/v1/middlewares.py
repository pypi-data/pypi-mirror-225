from starlette.middleware.base import BaseHTTPMiddleware

from news_toolkit_api.config.settings import NEWS_TOOLKIT_CACHE_CONTROL

CACHED_PATH = [
    "/api/v1/articles/",
    "/api/v1/feed",
    "/api/v1/subscriptions",
    "/api/v1//categories",
]
CACHE_CONTROL_VALUE = f"public, max-age={NEWS_TOOLKIT_CACHE_CONTROL}"


class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # cache-control is available under the condition
        if request.method == "GET" and any(
            request.url.path.startswith(path) for path in CACHED_PATH
        ):
            response.headers["Cache-Control"] = CACHE_CONTROL_VALUE
        return response
