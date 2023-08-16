import json

from e2xcore.handlers import E2xApiHandler
from e2xcore.utils import urljoin
from jupyter_client.kernelspec import KernelSpecManager
from nbgrader.server_extensions.formgrader.base import check_xsrf
from tornado import web

from ...managers import (
    AssignmentManager,
    PresetManager,
    TaskManager,
    TaskPoolManager,
    TemplateManager,
    WorksheetManager,
)
from ...utils.gitutils import get_author, set_author
from .base import ApiManageHandler


class KernelSpecHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.write(json.dumps(KernelSpecManager().get_all_specs()))


class GitAuthorHandler(E2xApiHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        self.write(json.dumps(get_author()))

    @web.authenticated
    @check_xsrf
    def post(self):
        data = self.get_json_body()
        name = data.get("name")
        email = data.get("email")
        self.write(json.dumps(set_author(name=name, email=email)))


api_url = urljoin("e2x", "authoring", "api")
name_regex = r"(?P<name>[^/]+)"
assignment_regex = r"(?P<assignment>[^/]+)"
default_handlers = [
    (
        urljoin(api_url, "assignments", "?"),
        ApiManageHandler,
        dict(
            manager_cls=AssignmentManager,
            actions=dict(
                get=dict(actions=["list"]),
            ),
        ),
    ),
    (
        urljoin(api_url, "worksheets", "?"),
        ApiManageHandler,
        dict(
            manager_cls=WorksheetManager,
            actions=dict(
                get=dict(actions=["get", "list"]),
                delete=dict(default="remove", actions=["remove"]),
                post=dict(default="create", actions=["create"]),
            ),
        ),
    ),
    (
        urljoin(api_url, "tasks", "?"),
        ApiManageHandler,
        dict(
            manager_cls=TaskManager,
            actions=dict(
                delete=dict(default="remove", actions=["remove"]),
                get=dict(
                    default="get", actions=["get", "list", "list_all", "git_diff"]
                ),
                post=dict(default="create", actions=["create"]),
                put=dict(actions=["copy", "rename", "commit"]),
            ),
        ),
    ),
    (
        urljoin(api_url, "templates", "?"),
        ApiManageHandler,
        dict(
            manager_cls=TemplateManager,
            actions=dict(
                delete=dict(default="remove", actions=["remove"]),
                get=dict(default="get", actions=["get", "list", "list_variables"]),
                post=dict(default="create", actions=["create"]),
                put=dict(actions=["copy", "rename"]),
            ),
        ),
    ),
    (
        urljoin(api_url, "pools", "?"),
        ApiManageHandler,
        dict(
            manager_cls=TaskPoolManager,
            actions=dict(
                delete=dict(default="remove", actions=["remove"]),
                get=dict(default="get", actions=["get", "list"]),
                post=dict(default="create", actions=["create"]),
                put=dict(actions=["copy", "rename", "turn_into_repository"]),
            ),
        ),
    ),
    (
        urljoin(api_url, "presets", "?"),
        ApiManageHandler,
        dict(
            manager_cls=PresetManager,
            actions=dict(
                get=dict(
                    actions=[
                        "list_question_presets",
                        "list_template_presets",
                        "get_question_preset",
                        "get_template_preset",
                    ]
                )
            ),
        ),
    ),
    (urljoin(api_url, "kernelspec"), KernelSpecHandler),
    (urljoin(api_url, "git", "author"), GitAuthorHandler),
]
