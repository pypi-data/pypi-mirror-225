import os
import sys

from e2xcore.utils import urljoin
from nbgrader.server_extensions.formgrader.base import (
    BaseHandler,
    check_notebook_dir,
    check_xsrf,
)
from tornado import web

app_url = urljoin("e2x", "authoring", "app")


class AuthoringHandler(BaseHandler):
    @web.authenticated
    @check_xsrf
    @check_notebook_dir
    def get(self):
        self.write(
            self.render(
                os.path.join("authoring", "index.html"),
                url_prefix=self.url_prefix,
                base_url=self.base_url,
                windows=(sys.prefix == "win32"),
            )
        )


default_handlers = [(urljoin(app_url, "?.*"), AuthoringHandler)]
