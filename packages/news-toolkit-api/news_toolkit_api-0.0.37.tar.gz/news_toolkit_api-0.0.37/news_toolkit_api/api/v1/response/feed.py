from dataclasses import dataclass
from datetime import datetime

from news_toolkit_api.news_blocks import (
    BlockType,
    NavigateToArticleAction,
    SectionHeaderBlock,
)


@dataclass(frozen=True)
class FeedArticleResponse:
    id: str
    title: str
    category: str
    image_url: str
    author: str | None
    published_at: datetime | None
    is_premium: bool
    type: BlockType
    action: NavigateToArticleAction


FeedType = list[SectionHeaderBlock | FeedArticleResponse]


@dataclass(frozen=True)
class FeedResponse:
    feed: FeedType
    next_cursor: str | None
