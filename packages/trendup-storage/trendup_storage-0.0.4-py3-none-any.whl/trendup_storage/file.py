from abc import abstractmethod

from attr import define


class StorageFile:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_extension(self) -> str:
        pass

    @abstractmethod
    def read(self) -> bytes:
        pass


@define
class StorageFileBasic(StorageFile):
    name: str
    extension: str
    content: bytes

    def get_name(self) -> str:
        return self.name

    def get_extension(self) -> str:
        return self.extension

    def read(self) -> bytes:
        return self.content
