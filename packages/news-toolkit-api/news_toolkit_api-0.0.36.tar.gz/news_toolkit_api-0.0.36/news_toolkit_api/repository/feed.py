from abc import ABCMeta

from news_toolkit_api.db import Feed
from news_toolkit_api.repository.interface import Repository


class FeedRepository(Repository[Feed], metaclass=ABCMeta):
    pass
