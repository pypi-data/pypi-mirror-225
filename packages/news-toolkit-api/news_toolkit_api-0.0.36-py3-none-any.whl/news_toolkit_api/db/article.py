from google.cloud import ndb

from news_toolkit_api.utils import sha3_hash


class RelatedArticle(ndb.Model):
    article_id = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    author = ndb.StringProperty()
    published_at = ndb.DateTimeProperty()


class Article(ndb.Model):
    article_id = ndb.StringProperty(required=True)
    cursor = ndb.StringProperty(required=True)
    next_cursor = ndb.StringProperty()
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(repeated=True)
    url = ndb.StringProperty(required=True)
    category = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty()
    author = ndb.StringProperty()
    published_at = ndb.DateTimeProperty()
    is_premium = ndb.BooleanProperty(default=False)
    is_preview = ndb.BooleanProperty(default=False)
    related_articles = ndb.StructuredProperty(RelatedArticle, repeated=True)
    created_at = ndb.DateTimeProperty(required=True)

    @property
    def id(self) -> str:
        return sha3_hash(f"{self.article_id}&{self.cursor}")
