from attr import define


@define
class StorageReference:
    env: str
    id: str
