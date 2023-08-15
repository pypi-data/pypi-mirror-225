from google.cloud import ndb

from news_toolkit_api.utils import sha3_hash


class FeedArticle(ndb.Model):
    article_id = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty(required=True)
    subtitle = ndb.StringProperty()
    author = ndb.StringProperty()
    published_at = ndb.DateTimeProperty()


class Feed(ndb.Model):
    category = ndb.StringProperty(required=True)
    cursor = ndb.StringProperty(required=True)
    next_cursor = ndb.StringProperty()
    feed = ndb.StructuredProperty(FeedArticle, repeated=True)
    created_at = ndb.DateTimeProperty(required=True)

    @property
    def id(self) -> str:
        return sha3_hash(f"{self.category}&{self.cursor}")
