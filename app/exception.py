from uuid import UUID


class NotFoundError(Exception):
    def __init__(self, id_: int | str | None | UUID = None, object_: str = "Object"):
        self.id_ = id_
        self.details = f"{object_} {id_} not found."
