from sqlalchemy import UUID


class LassenUUID(UUID):
    """
    Hack to avoid namespace collisions between uuid.UUID and sqlalchemy.UUID
    TODO: Remove this once we have collision detection

    """

    pass
