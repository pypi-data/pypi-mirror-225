from dataclasses import dataclass

from news_toolkit_api.news_blocks import (
    ArticleIntroductionBlock,
    BannerAdContent,
    TextLeadParagraphBlock,
)

ContentType = list[ArticleIntroductionBlock | TextLeadParagraphBlock | BannerAdContent]


@dataclass(frozen=True)
class ArticleResponse:
    title: str
    content: ContentType
    url: str
    is_premium: bool
    is_preview: bool
    next_cursor: str
