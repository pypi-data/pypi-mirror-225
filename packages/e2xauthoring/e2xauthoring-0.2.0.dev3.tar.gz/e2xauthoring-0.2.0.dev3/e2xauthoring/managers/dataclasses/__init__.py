import dataclasses
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class JSONDataClass:
    def json(self):
        return dataclasses.asdict(self)


@dataclass
class Template(JSONDataClass):
    name: str


@dataclass
class TaskPool(JSONDataClass):
    name: str
    n_tasks: int
    is_repo: bool = False


@dataclass
class Task(JSONDataClass):
    name: str
    pool: str
    points: int
    n_questions: int
    git_status: Dict


@dataclass
class Exercise(JSONDataClass):
    name: str
    assignment: str


@dataclass
class SuccessMessage(JSONDataClass):
    success: bool = True
    message: str = ""
    data: Any = None


@dataclass
class ErrorMessage(JSONDataClass):
    success: bool = False
    error: str = ""
