import tempfile
from pathlib import Path
from unittest import TestCase

from trendup_storage.file import StorageFileBasic
from trendup_storage.trendup_storage.local.local_storage import FileStorageLocal


class TestFileStorageLocal(TestCase):

    def setUp(self) -> None:
        self.path = Path(tempfile.mkdtemp())
        self.storage = FileStorageLocal(directory=self.path)

    def test_should_save_file(self):
        self.assertSaveAndLoad()

    def test_should_create_directory_if_not_exists(self):
        self.path.rmdir()
        self.assertSaveAndLoad()

    def assertSaveAndLoad(self):
        file = StorageFileBasic(name="hello", extension="txt", content="content".encode())
        reference = self.storage.save(file)
        loaded = self.storage.load(reference)

        self.assertEqual(file.name, loaded.get_name())
        self.assertEqual(file.extension, loaded.get_extension())
        self.assertEqual(file.content, loaded.read())
