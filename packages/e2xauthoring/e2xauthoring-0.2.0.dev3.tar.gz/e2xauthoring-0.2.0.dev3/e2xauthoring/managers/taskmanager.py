import os
import shutil

import nbformat
from e2xcore.utils.nbgrader_cells import is_nbgrader_cell, new_read_only_cell
from nbformat.v4 import new_notebook
from traitlets import Unicode

from ..utils.gitutils import commit_path, vcs_status
from .base import BaseManager
from .dataclasses import Task
from .taskpoolmanager import TaskPoolManager


class TaskManager(BaseManager):
    directory = Unicode(
        "pools", help="The relative directory where the pools are stored"
    )

    def __get_task_info(self, task, pool):
        base_path = os.path.join(self.base_path, pool)
        notebooks = [
            file
            for file in os.listdir(os.path.join(base_path, task))
            if file.endswith(".ipynb")
        ]

        points = 0
        questions = 0

        for notebook in notebooks:
            nb = nbformat.read(os.path.join(base_path, task, notebook), as_version=4)
            for cell in nb.cells:
                if "nbgrader" in cell.metadata and cell.metadata.nbgrader.grade:
                    points += cell.metadata.nbgrader.points
                    questions += 1
        return points, questions

    def commit(self, pool, task, message):
        path = os.path.join(self.base_path, pool, task)
        git_status = self.git_status(pool, task)
        assert git_status is not None, f"Path {path} is not part of a git repository."
        if git_status["status"] == "unchanged":
            return "Nothing to commit. No files have been changed."

        commit_okay = commit_path(
            git_status["repo"], path, add_if_untracked=True, message=message
        )
        assert commit_okay, "There was an error during the commit process."

    def git_status(self, pool, task):
        path = os.path.join(self.base_path, pool, task)
        git_status = vcs_status(path, relative=True)
        if git_status["repo"] is None:
            return dict(status="not version controlled")
        changed_files = (
            git_status["untracked"] + git_status["unstaged"] + git_status["staged"]
        )
        git_status["status"] = "modified" if len(changed_files) > 0 else "unchanged"
        return git_status

    def git_diff(self, pool, task, file):
        path = os.path.join(self.base_path, pool, task, file)
        assert os.path.exists(path), f"Path {path} does not exist"
        git_status = vcs_status(path)
        assert (
            git_status["repo"] is not None
        ), f"Path {path} is not version controlled or not added"
        relpath = os.path.relpath(path, start=git_status["repo"].working_tree_dir)
        return dict(
            path=path,
            diff=git_status["repo"]
            .git.diff(relpath, color=True)
            .replace("\n", "<br/>"),
        )

    def get(self, pool: str, name: str):
        path = os.path.join(self.base_path, pool, name)
        assert os.path.exists(path), "The task does not exists"
        points, n_questions = self.__get_task_info(name, pool)
        git_status = self.git_status(pool, name)
        if "repo" in git_status:
            del git_status["repo"]
        return Task(
            name=name,
            pool=pool,
            points=points,
            n_questions=n_questions,
            git_status=git_status,
        )

    def create(self, pool: str, name: str):
        assert self.is_valid_name(name), "The name is invalid!"
        path = os.path.join(self.base_path, pool, name)
        assert not os.path.exists(
            path
        ), f"A task with the name {name} already exists in the pool {pool}!"
        self.log.info(f"Creating new task with name {name}")
        os.makedirs(os.path.join(path, "img"), exist_ok=True)
        os.makedirs(os.path.join(path, "data"), exist_ok=True)
        nb = new_notebook(metadata=dict(nbassignment=dict(type="task")))
        cell = new_read_only_cell(
            grade_id=f"{name}_Header",
            source=(
                f"# {name}\n"
                "Here you should give the general information about the task.\n"
                "Then add questions via the menu above.\n"
                "A task should be self contained"
            ),
        )
        nb.cells.append(cell)
        nbformat.write(nb, os.path.join(path, f"{name}.ipynb"))

    def remove(self, pool, name):
        path = os.path.join(self.base_path, pool, name)
        assert os.path.exists(
            path
        ), f"No task with the name {name} from pool {pool} exists."
        shutil.rmtree(path)

    def list(self, pool):
        tasks = []
        path = os.path.join(self.base_path, pool)
        assert os.path.exists(path), f"No pool with the name {pool} exists."
        for task_dir in self.listdir(os.path.join(self.base_path, pool)):
            points, n_questions = self.__get_task_info(task_dir, pool)
            git_status = self.git_status(pool, task_dir)
            if "repo" in git_status:
                del git_status["repo"]
            tasks.append(
                Task(
                    name=task_dir,
                    pool=pool,
                    points=points,
                    n_questions=n_questions,
                    git_status=git_status,
                )
            )
        return tasks

    def list_all(self):
        pool_manager = TaskPoolManager(self.coursedir)
        tasks = []
        for pool in pool_manager.list():
            tasks.extend(self.list(pool.name))
        return tasks

    def copy(self, old_name: str, new_name: str, pool: str = ""):
        src = os.path.join(pool, old_name)
        dst = os.path.join(pool, new_name)
        super().copy(src, dst)
        dst_path = os.path.join(self.base_path, dst)
        shutil.move(
            os.path.join(dst_path, f"{old_name}.ipynb"),
            os.path.join(dst_path, f"{new_name}.ipynb"),
        )
        nb_path = os.path.join(dst_path, f"{new_name}.ipynb")
        nb = nbformat.read(nb_path, as_version=nbformat.NO_CONVERT)
        for cell in nb.cells:
            if is_nbgrader_cell(cell):
                grade_id = cell.metadata.nbgrader.grade_id
                cell.metadata.nbgrader.grade_id = grade_id.replace(old_name, new_name)
        nbformat.write(nb, nb_path)

    def rename(self, old_name: str, new_name: str, pool: str = ""):
        self.copy(old_name, new_name, pool)
        self.remove(pool, old_name)
