import uuid
from pathlib import Path
from typing import Optional

from attr import define

from trendup_storage.file import StorageFile, StorageFileBasic
from trendup_storage.file_storage import FileStorage
from trendup_storage.models import StorageReference


@define
class FileStorageLocal(FileStorage):
    directory: Path

    def save(self, file: StorageFile) -> StorageReference:
        random_id = uuid.uuid4().__str__()
        path = self.directory / random_id / f"{file.get_name()}.{file.get_extension()}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(file.read())
        return StorageReference(env="LOCAL", id=random_id)

    def load(self, reference: StorageReference) -> Optional[StorageFile]:
        path = self.directory / reference.id

        if not path.exists():
            return None

        file = path.glob("*").__next__()
        return StorageFileBasic(
            name=file.stem,
            extension=file.suffix.lstrip("."),
            content=file.read_bytes()
        )
