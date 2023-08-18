import uuid

import uuid_extensions


def uuid7() -> uuid.UUID:
    """
    Generate a UUID version 7.
    :return: UUID version 7.
    """
    return uuid_extensions.uuid7()
