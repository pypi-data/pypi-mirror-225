import os
import re
import shutil
from abc import abstractmethod
from typing import List

from nbgrader.coursedir import CourseDirectory
from traitlets import Unicode
from traitlets.config import LoggingConfigurable


class BaseManager(LoggingConfigurable):
    directory = Unicode(".", help="The directory of the items to manage")

    def __init__(self, coursedir: CourseDirectory) -> None:
        self.coursedir = coursedir
        self.__pattern = re.compile(r"^\w+[\w\s]*\w+$")

    @property
    def base_path(self):
        return self.coursedir.format_path(self.directory, ".", ".")

    def is_valid_name(self, name) -> bool:
        return self.__pattern.match(name) is not None

    def listdir(self, path: str) -> List[str]:
        return [
            directory for directory in os.listdir(path) if not directory.startswith(".")
        ]

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def remove(self, **kwargs):
        pass

    @abstractmethod
    def list(self, **kwargs):
        pass

    def copy(self, old_name: str, new_name: str):
        src_path = os.path.join(self.base_path, old_name)
        dst_path = os.path.join(self.base_path, new_name)
        assert os.path.exists(src_path), "Source does not exist."
        assert not os.path.exists(
            dst_path
        ), "Destination already exists. Please delete first or choose a new name."
        shutil.copytree(src_path, dst_path)

    def rename(self, old_name: str, new_name: str):
        self.copy(old_name, new_name)
        self.remove(old_name)
