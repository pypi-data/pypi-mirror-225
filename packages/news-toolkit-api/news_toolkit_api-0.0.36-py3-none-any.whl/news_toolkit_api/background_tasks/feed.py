from google.cloud import ndb

from news_toolkit_api.background_tasks.article import background_task_article
from news_toolkit_api.background_tasks.utils import async_timeout
from news_toolkit_api.db import Feed
from news_toolkit_api.repository import ArticleRepository, FeedRepository


@async_timeout()
async def background_task_feed(
    client: ndb.Client,
    article_repository: ArticleRepository,
    feed_repository: FeedRepository,
    category: str,
    cursor: str,
) -> Feed | None:
    feed = await feed_repository.fetch_content(category, cursor)
    if not feed:
        return None

    for feed_article in feed.feed:
        await background_task_article(
            client, article_repository, feed_article.article_id, "", 1
        )

    with client.context():
        feed.key = ndb.Key(Feed, feed.id)
        feed.put()
    return feed
