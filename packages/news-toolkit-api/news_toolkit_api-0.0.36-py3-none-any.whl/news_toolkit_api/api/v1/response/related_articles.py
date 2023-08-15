from dataclasses import dataclass
from datetime import datetime

from news_toolkit_api.news_blocks import BlockType, NavigateToArticleAction


@dataclass(frozen=True)
class RelatedArticleResponse:
    id: str
    title: str
    category: str
    image_url: str
    author: str | None
    published_at: datetime | None
    is_premium: bool
    type: BlockType
    action: NavigateToArticleAction


@dataclass(frozen=True)
class RelatedArticlesResponse:
    related_articles: list[RelatedArticleResponse]
    next_cursor: str | None
