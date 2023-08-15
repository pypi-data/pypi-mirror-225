import argparse

from google.cloud import ndb

from news_toolkit_api.db import Category
from news_toolkit_api.utils import sha3_hash

client = ndb.Client()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--categories", nargs="+", default=list)
    args = parser.parse_args()

    with client.context():
        categories = [
            Category(
                key=ndb.Key(Category, sha3_hash(category)),
                name=category,
                order=i,
            )
            for i, category in enumerate(args.categories)
        ]
        ndb.put_multi(categories)
