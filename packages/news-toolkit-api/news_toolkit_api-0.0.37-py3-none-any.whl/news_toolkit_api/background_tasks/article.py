from google.cloud import ndb

from news_toolkit_api.background_tasks.utils import async_timeout
from news_toolkit_api.config.settings import NEWS_TOOLKIT_MAX_RECURSION_DEPTH
from news_toolkit_api.db.article import Article
from news_toolkit_api.repository.article import ArticleRepository


@async_timeout()
async def background_task_article(
    client: ndb.Client,
    article_repository: ArticleRepository,
    article_id: str,
    cursor: str,
    depth: int = 0,
) -> Article | None:
    article = await article_repository.fetch_content(article_id, cursor)
    if not article:
        return None

    with client.context():
        article.key = ndb.Key(Article, article.id)
        article.put()

    if depth < NEWS_TOOLKIT_MAX_RECURSION_DEPTH:
        if article.next_cursor:
            await background_task_article(
                client,
                article_repository,
                article.article_id,
                article.next_cursor,
                depth + 1,
            )
        for related_article in article.related_articles:
            await background_task_article(
                client, article_repository, related_article.article_id, "", depth + 1
            )

    return article
