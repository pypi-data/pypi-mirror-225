from abc import ABCMeta, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from news_toolkit_api.db import Article, RelatedArticle
from news_toolkit_api.repository.interface import Repository


class ArticleRepository(Repository[Article], metaclass=ABCMeta):
    @abstractmethod
    def parse_title(self, soup: BeautifulSoup) -> str | None:
        pass

    @abstractmethod
    def parse_content(self, soup: BeautifulSoup) -> list[str] | None:
        pass

    @abstractmethod
    def parse_category(self, soup: BeautifulSoup) -> str | None:
        pass

    @abstractmethod
    def parse_image_url(self, soup: BeautifulSoup) -> str | None:
        pass

    @abstractmethod
    def parse_author(self, soup: BeautifulSoup) -> str | None:
        pass

    @abstractmethod
    def parse_published_at(self, soup: BeautifulSoup) -> datetime | None:
        pass

    @abstractmethod
    def parse_related_articles(self, soup: BeautifulSoup) -> list[RelatedArticle]:
        pass

    @abstractmethod
    def parse_next_cursor(self, soup: BeautifulSoup) -> str | None:
        pass

    def parse(self, soup: BeautifulSoup, id: str, cursor: str) -> Article | None:
        title = self.parse_title(soup)
        content = self.parse_content(soup)
        category = self.parse_category(soup)
        if not title or not content or not category:
            return None

        return Article(
            article_id=id,
            cursor=cursor,
            next_cursor=self.parse_next_cursor(soup),
            title=title,
            content=content,
            url=self.build_url(id, cursor),
            category=category,
            image_url=self.parse_image_url(soup),
            author=self.parse_author(soup),
            published_at=self.parse_published_at(soup),
            related_articles=self.parse_related_articles(soup),
            is_premium=False,
            is_preview=False,
            created_at=datetime.utcnow(),
        )
