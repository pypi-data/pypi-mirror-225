import os
import shutil

from traitlets import Unicode

from ..utils.gitutils import create_repository, is_version_controlled
from .base import BaseManager
from .dataclasses import TaskPool


class TaskPoolManager(BaseManager):
    directory = Unicode(
        "pools", help="The relative directory where the pools are stored"
    )

    def __get_n_tasks(self, name) -> int:
        return len(
            [
                d
                for d in os.listdir(os.path.join(self.base_path, name))
                if not d.startswith(".")
            ]
        )

    def turn_into_repository(self, pool):
        path = os.path.join(self.base_path, pool)
        assert os.path.exists(path) and os.path.isdir(
            path
        ), f"The pool {pool} does not exist or is not a directory."
        repo = create_repository(path)
        assert (
            repo is not None
        ), f"There was an issue turning the pool {pool} into a repository!"

    def get(self, name: str):
        path = os.path.join(self.base_path, name)
        assert os.path.exists(path), f"A pool with the name {name} does not exists!"
        return TaskPool(
            name=name,
            n_tasks=self.__get_n_tasks(name),
            is_repo=is_version_controlled(path),
        )

    def create(self, name: str, init_repository: bool = False):
        assert self.is_valid_name(name), "The name is invalid!"
        path = os.path.join(self.base_path, name)
        assert not os.path.exists(path), f"A pool with the name {name} already exists!"
        os.makedirs(path, exist_ok=True)
        if init_repository:
            return self.turn_into_repository(name)

    def remove(self, name):
        path = os.path.join(self.base_path, name)
        assert os.path.exists(path), f"The task pool {name} does not exist"
        shutil.rmtree(path)

    def list(self):
        assert os.path.exists(self.base_path), "Pool directory does not exist."
        return [
            TaskPool(
                name=pool_dir,
                n_tasks=self.__get_n_tasks(pool_dir),
                is_repo=is_version_controlled(os.path.join(self.base_path, pool_dir)),
            )
            for pool_dir in self.listdir(self.base_path)
        ]
