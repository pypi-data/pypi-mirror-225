from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ArticleIntroductionBlock:
    title: str
    category: str
    author: str | None
    published_at: datetime | None
    image_url: str | None
    is_premium: bool
    type: str = "__article_introduction__"
