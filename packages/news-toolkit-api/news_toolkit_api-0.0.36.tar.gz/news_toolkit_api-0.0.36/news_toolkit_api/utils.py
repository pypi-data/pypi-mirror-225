import hashlib
from datetime import datetime, timedelta

from news_toolkit_api.config.settings import NEWS_TOOLKIT_UPDATE_INTERVAL_MINUTES


def sha3_hash(data: str) -> str:
    """
    Computes the SHA-3 256-bit hash of the given string.

    :param data: The string to be hashed.
    :return: The SHA-3 256-bit hash as a hexadecimal string.
    """
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(data.encode("utf-8"))
    return sha3_256.hexdigest()


def needs_update(last_updated_time: datetime) -> bool:
    """
    Check if the provided datetime is older than the allowed interval.

    :param last_updated_time: The datetime to check against.
    :return: True if an update is required, False otherwise.
    """
    current_time = datetime.utcnow()
    deadline_time = current_time - timedelta(
        minutes=NEWS_TOOLKIT_UPDATE_INTERVAL_MINUTES
    )
    return last_updated_time < deadline_time
