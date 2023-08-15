import asyncio
import logging
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup

from news_toolkit_api.config.settings import (
    NEWS_TOOLKIT_REQUEST_TIMEOUT,
    NEWS_TOOLKIT_REQUEST_USER_AGENT,
)

Content = TypeVar("Content")


class Repository(Generic[Content], metaclass=ABCMeta):
    @abstractmethod
    def build_url(self, id: str, cursor: str) -> str:
        pass

    @abstractmethod
    def parse(self, soup: BeautifulSoup, id: str, cursor: str) -> Content | None:
        pass

    @staticmethod
    async def fetch_html(url: str) -> str | None:
        try:
            async with aiohttp.ClientSession(
                timeout=ClientTimeout(NEWS_TOOLKIT_REQUEST_TIMEOUT),
                headers={"User-Agent": NEWS_TOOLKIT_REQUEST_USER_AGENT},
            ) as session:
                async with session.get(url) as res:
                    res.raise_for_status()
                    return await res.text()
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching the url {url}: {e}")
            return None
        except asyncio.TimeoutError:
            logging.error(f"Timeout while fetching the url {url}.")
            return None

    async def fetch_content(self, id: str, cursor: str) -> Content | None:
        html_text = await self.fetch_html(self.build_url(id, cursor))
        if not html_text:
            return None

        soup = BeautifulSoup(html_text, features="html5lib")
        if not soup:
            return None

        return self.parse(soup, id, cursor)
