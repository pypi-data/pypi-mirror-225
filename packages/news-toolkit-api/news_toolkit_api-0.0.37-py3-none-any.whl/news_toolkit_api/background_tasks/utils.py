import asyncio
import logging

from news_toolkit_api.config.settings import NEWS_TOOLKIT_BACKGROUND_TASK_TIMEOUT


def async_timeout(timeout: int = NEWS_TOOLKIT_BACKGROUND_TASK_TIMEOUT):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError as e:
                logging.error("Task timed out.")
                raise e

        return wrapper

    return decorator
