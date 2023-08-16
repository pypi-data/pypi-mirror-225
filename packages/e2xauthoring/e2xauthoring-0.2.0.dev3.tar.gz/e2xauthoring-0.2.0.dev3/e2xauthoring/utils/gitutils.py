import os
import shutil
from typing import Dict, List, Union

from git import Actor, BadName, Git, GitCommandError, InvalidGitRepositoryError, Repo


def is_parent_path(parent_path: str, child_path: str) -> bool:
    """Check if a path is a parent of another path

    Args:
        parent_path (str): The potential parent path
        child_path (str): The path to test
    Returns:
        bool: True if child_path is a sub directory of parent_path
    """
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)
    return os.path.commonpath([parent_path]) == os.path.commonpath(
        [parent_path, child_path]
    )


def is_version_controlled(path: str) -> bool:
    """Test whether a path is part of a git repository

    Args:
        path (str): Path to check for

    Returns:
        bool: True if part of a git repository
    """
    try:
        Repo(path, search_parent_directories=True)
        return True
    except InvalidGitRepositoryError:
        return False


def vcs_status(path: str, relative: bool = False) -> Dict[str, Union[List[str], bool]]:
    """Get the version control status of a path

    Args:
        path (str): Path to check
        relative (bool, optional): Turn paths into relative paths starting at path.
                                   Defaults to False.

    Returns:
        dict: A dictionary containing untracked files, unstaged files and staged files
              under the path
    """
    if not is_version_controlled(path):
        return dict(repo=None)
    repo = Repo(path, search_parent_directories=True)
    # Get the general status of the repository
    status = dict(
        repo=repo,
        untracked=repo.untracked_files,
        staged=[],
        unstaged=[item.a_path for item in repo.index.diff(None)],
    )
    try:
        status["staged"] = [item.a_path for item in repo.index.diff("HEAD")]
    except BadName:
        pass
    # Filter out all files that are not a sub path of path
    for field in ["untracked", "unstaged", "staged"]:
        status[field] = [
            f
            for f in status[field]
            if is_parent_path(path, os.path.join(repo.working_tree_dir, f))
        ]
        if relative:
            status[field] = [
                os.path.relpath(os.path.join(repo.working_tree_dir, f), start=path)
                for f in status[field]
            ]

    return status


def commit_path(
    repo: Repo,
    path: str,
    add_if_untracked=False,
    message: str = None,
    author: Actor = None,
) -> bool:
    """Commit all files in a given path

    Args:
        repo (Repo): A git repository instance
        path (str): The path to commit
        add_if_untracked (bool, optional): If untracked files should be added before committing.
        Defaults to False.
        message (str, optional): The commit message. Defaults to None.
        author (Actor, optional): An author object to specify the author of the commit.
                                  If not set the global git author will be used. Defaults to None.

    Returns:
        bool: status
    """
    path = os.path.relpath(os.path.abspath(path), start=repo.working_tree_dir)
    if add_if_untracked:
        repo.git.add(path)
    if message is None:
        message = f"Update {path}"
    command = [
        f"-m '{message}'",
    ]
    if author is not None:
        command.append(f"--author='{author.name} <{author.email}'")
    command.append(path)
    repo.git.commit(command)
    return True


def create_repository(path: str, exists_ok: bool = True, author: Actor = None) -> Repo:
    """Create a repository
    Intitializes the repository with a gitignore if it does not exists

    Args:
        path (str): The base path of the repository
        exists_ok (bool, optional): If the repository already exists do not throw an exception.
                                    Defaults to True.
        author (Actor, optional): An author object to specify the author of the commit.
                                  If not set the global git author will be used. Defaults to None.

    Returns:
        Repo: _description_
    """
    path = os.path.abspath(path)
    repo = None
    try:
        repo = Repo(path, search_parent_directories=True)
        assert exists_ok, (
            f"A repository already exists at {repo.working_tree_dir}."
            "Run with option exists_ok=True to ignore."
        )
        return repo
    except InvalidGitRepositoryError:
        repo = Repo.init(path)
    here = os.path.dirname(__file__)
    gitignore = ".gitignore"
    shutil.copy(
        os.path.join(here, "..", "assets", gitignore),
        os.path.join(repo.working_tree_dir, gitignore),
    )
    repo.git.add([gitignore])
    command = [f"-m 'Add {gitignore}'"]
    if author is not None:
        command.append(f"--author='{author.name} <{author.email}'")
    command.append(gitignore)
    repo.git.commit(command)
    return repo


def get_author() -> Dict[str, str]:
    """Get the current global git author

    Returns:
        Dict[str, str]: A dictionary containing the name and email address of the author
    """
    try:
        return dict(
            name=Git().config(["--global", "user.name"]),
            email=Git().config(["--global", "user.email"]),
        )
    except GitCommandError:
        pass


def set_author(name: str, email: str) -> Dict[str, Union[str, bool]]:
    """Set the global git author

    Args:
        name (str): The name of the author
        email (str): The email address of the author

    Returns:
        Dict[str, Union[str, bool]]: A dictionary containing status information
    """
    try:
        Git().config(["--global", "user.name", name])
        Git().config(["--global", "user.email", email])
        return dict(success=True)
    except GitCommandError:
        return dict(success=False, message="There was an error setting the author")
