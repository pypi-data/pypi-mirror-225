from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible

from ._mega import Mega


Url = str
MegaNodeObj = Union[Dict[str, Any], Tuple[Union[str, Dict[str, Any]]]]

client = Mega()


@deconstructible
class MegaDriveStorage(Storage):

    def __init__(self, mega_email, mega_password, *args, **kwargs):
        self.mega = client.login(email=mega_email, password=mega_password)
        super().__init__(*args, **kwargs)

    @lru_cache()
    def _open(self, name: str, mode: str = "rb") -> ContentFile:
        url: Url = self._get_url(name)
        response = requests.get(url)
        response.raise_for_status()
        file: ContentFile = ContentFile(response.content)
        file.name = name
        file.mode = mode
        return file

    def _save(self, name: str, content: InMemoryUploadedFile) -> str:
        response: MegaNodeObj = self.upload(name, content)
        return response["f"][0].get("h")

    def upload(self, name: str, content: InMemoryUploadedFile) -> MegaNodeObj:
        filename, folder = self.get_filename_and_folder(name)
        folder_dest: str | None = self.get_or_create_folder(
            folder) if folder else None
        response: MegaNodeObj = self.mega.upload(
            content, folder_dest, filename)
        return response

    def get_filename_and_folder(self, name) -> Tuple[str | None]:
        path: Path = Path(name)
        filename: str = path.name
        folder: str = str(path.parent)
        return (path.name, folder if folder != "." else None)

    def get_or_create_folder(self, path: str) -> str:
        """Return the exist folder  id.  if not exist then it will create new folder"""

        initial_path: List[str] = path.split("/")
        folder: str | None = None
        new_child_folder: str = ""

        while len(initial_path):
            found_folder: MegaNodeObj | None = self.mega.find_path_descriptor(
                "/".join(initial_path)
            )
            if found_folder:
                folder = found_folder
                break
            new_child_folder += f"{initial_path[-1]}/"
            initial_path = initial_path[: len(initial_path) - 1]

        if folder:
            if new_child_folder:
                child_folder: MegaNodeObj = self.mega.create_folder(
                    new_child_folder, dest=folder
                )
                return self.get_created_folder_id(child_folder)
            return folder

        new_folder: MegaNodeObj = self.mega.create_folder(path)
        return self.get_created_folder_id(new_folder)

    def get_created_folder_id(self, folder: MegaNodeObj) -> str:
        """Return the folder  id of the created  folder"""
        return list(folder.values())[-1]

    def delete(self, name: str) -> None:
        """Delete the file from mega drive storage to the given name"""

        assert bool(name), 'invalid file name'

        self.mega.delete(name)

    @lru_cache()
    def exists(self, name: str) -> bool:
        """check weather the file exists or not"""

        file: MegaNodeObj | None = self.mega.find(
            Path(name).name, exclude_deleted=True)
        return file is not None

    def empty_trash(self) -> None:
        """deletes the bin files"""

        self.mega.empty_trash()

    @lru_cache()
    def _get_url(self, name: str) -> Url:
        file: MegaNodeObj | None = self.mega.find(handle=name)
        return self.mega.get_link((name, file)) if file else ""

    def url(self, name: str) -> Url:
        """Return download link of mega drive storage"""

        return self._get_url(name)

    @lru_cache()
    def size(self, name: str) -> int:
        """ Return filesize in bytes..."""

        file: MegaNodeObj | None = self.mega.find(
            handle=name, exclude_deleted=True)
        return file.get("s") if file else 0
