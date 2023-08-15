from google.cloud import ndb


def get_client():
    client = ndb.Client()
    try:
        yield client
    finally:
        client.close()
