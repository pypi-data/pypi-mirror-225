import os

from e2xcore import BaseApp
from nbgrader.apps.baseapp import NbGrader
from tornado import web

from .handlers.apihandlers import default_handlers
from .handlers.handlers import default_handlers as handlers


class AuthoringApp(NbGrader, BaseApp):
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(template_path, "authoring", "static")

    def __init__(self, **kwargs) -> None:
        NbGrader.__init__(self, **kwargs)
        BaseApp.__init__(self, **kwargs)

    def load_app(self) -> None:
        self.log.info("Loading the e2xgrader git authoring app")
        self.add_template_path(self.template_path)
        self.add_handlers(default_handlers)
        self.add_handlers(
            [
                (
                    r"/e2x/authoring/static/(.*)",
                    web.StaticFileHandler,
                    dict(path=self.static_path),
                )
            ]
        )
        self.add_handlers(handlers)
