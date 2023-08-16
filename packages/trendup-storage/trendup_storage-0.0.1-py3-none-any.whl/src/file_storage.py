from abc import abstractmethod
from typing import Optional

from src.trendup_storage.file import StorageFile
from src.trendup_storage.models import StorageReference


class FileStorage:

    @abstractmethod
    def load(self, reference: StorageReference) -> Optional[StorageFile]:
        pass

    @abstractmethod
    def save(self, file: StorageFile) -> StorageReference:
        pass
