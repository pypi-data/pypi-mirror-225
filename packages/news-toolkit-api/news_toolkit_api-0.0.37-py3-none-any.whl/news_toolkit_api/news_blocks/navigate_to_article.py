from dataclasses import dataclass


@dataclass(frozen=True)
class NavigateToArticleAction:
    article_id: str
    type: str = "__navigate_to_article__"
