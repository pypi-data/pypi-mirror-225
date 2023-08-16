import os
import shutil

import nbformat
from e2xcore.utils.nbgrader_cells import new_read_only_cell
from nbformat.v4 import new_notebook
from traitlets import Unicode

from e2xauthoring.utils.notebookvariableextractor import NotebookVariableExtractor

from .base import BaseManager
from .dataclasses import Template


class TemplateManager(BaseManager):
    directory = Unicode(
        "templates", help="The relative directory where the templates are stored"
    )

    def get(self, name: str):
        path = os.path.join(self.base_path, name)
        assert os.path.exists(path), f"A template with the name {name} does not exists!"
        return Template(name=name)

    def create(self, name: str):
        assert self.is_valid_name(name), "The name is invalid!"
        path = os.path.join(self.base_path, name)
        assert not os.path.exists(
            path
        ), f"A template with the name {name} already exists!"
        self.log.info(f"Creating new template with name {name}")
        os.makedirs(os.path.join(self.base_path, name, "img"), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, name, "data"), exist_ok=True)
        nb = new_notebook(metadata=dict(nbassignment=dict(type="template")))
        cell = new_read_only_cell(
            grade_id="HeaderA",
            source=(
                "### This is a header cell\n\n"
                "It will always appear at the top of the notebook"
            ),
        )
        cell.metadata["nbassignment"] = dict(type="header")
        nb.cells.append(cell)
        nbformat.write(nb, os.path.join(self.base_path, name, f"{name}.ipynb"))

    def remove(self, name: str):
        path = os.path.join(self.base_path, name)
        assert os.path.exists(path), f"The template {name} does not exist."
        shutil.rmtree(path)

    def list(self):
        assert os.path.exists(self.base_path), "Template directory not found."
        templates = [
            Template(name=template_dir) for template_dir in self.listdir(self.base_path)
        ]
        return templates

    def list_variables(self, name):
        path = os.path.join(self.base_path, name, f"{name}.ipynb")
        assert os.path.exists(path), f"The template {name} does not exist."
        return NotebookVariableExtractor().extract(path)

    def copy(self, old_name: str, new_name: str):
        super().copy(old_name, new_name)
        dst_path = os.path.join(self.base_path, new_name)
        shutil.move(
            os.path.join(dst_path, f"{old_name}.ipynb"),
            os.path.join(dst_path, f"{new_name}.ipynb"),
        )
