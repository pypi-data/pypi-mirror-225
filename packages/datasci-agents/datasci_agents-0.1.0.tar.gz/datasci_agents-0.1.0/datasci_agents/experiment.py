import os
from typing import Optional
from copy import deepcopy
import nbformat as nbf
from nbformat.notebooknode import NotebookNode
from jupyter_client.manager import KernelManager


class PendingExperiment:
    def __init__(
        self,
        name: str,
        specification: str,
    ):
        self.name = name
        self.specification = specification


class Experiment:
    def __init__(
        self,
        notebook_path: str,
    ):
        filename = os.path.basename(notebook_path)
        assert filename.endswith(
            ".ipynb"
        ), f"Notebook {notebook_path} should have .ipynb extension"
        assert os.path.exists(notebook_path), f"Notebook {notebook_path} does not exist"

        self.name = filename[: -len(".ipynb")]
        self.notebook_path = notebook_path
        self.load_notebook()

    @classmethod
    def from_pending_experiment(
        cls, pending_experiment: PendingExperiment, experiment_dir: str
    ) -> "Experiment":
        notebook_path = os.path.join(experiment_dir, f"{pending_experiment.name}.ipynb")
        experiment = cls.create_empty_experiment(notebook_path)
        experiment.add_markdown_cell(pending_experiment.specification)
        experiment.save_notebook()
        return experiment

    @classmethod
    def create_empty_experiment(cls, notebook_path: str) -> "Experiment":
        nb = nbf.v4.new_notebook()
        dirname = os.path.dirname(notebook_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(os.path.dirname(notebook_path))
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        experiment = cls(notebook_path)
        return experiment

    def load_notebook(self) -> None:
        with open(self.notebook_path, "r", encoding="utf-8") as f:
            self.notebook = nbf.read(f, as_version=4)

    def save_notebook(self) -> None:
        with open(self.notebook_path, "w", encoding="utf-8") as f:
            nbf.write(self.notebook, f)

    def add_code_cell(self, source: str, outputs: Optional[list]) -> None:
        cell = nbf.v4.new_code_cell(source=source, outputs=outputs)
        self.notebook.cells.append(cell)

    def add_markdown_cell(self, source: str) -> None:
        cell = nbf.v4.new_markdown_cell(source=source)
        self.notebook.cells.append(cell)

    def remove_trailing_empty_cells(self) -> None:
        while (
            len(self.notebook.cells) > 0
            and self.notebook.cells[-1].source.strip() == ""
        ):
            self.notebook.cells.pop()

    @property
    def cells(self) -> list:
        return self.notebook.cells

    @property
    def specification(self) -> str:
        # Experiment specification is the first cell in the notebook (must be MD)
        first_cell = self.notebook.cells[0]
        if first_cell["cell_type"] != "markdown":
            raise ValueError("First cell in the notebook should be markdown")
        specification = first_cell["source"]
        assert specification, "Experiment specification should not be empty"
        return specification

    @property
    def conclusion(self) -> Optional[str]:
        # Experiment conclusion is the last non-empty cell in the notebook that starts with "# Conclusion"
        nonempty_md_contents = [
            cell["source"]
            for cell in self.notebook.cells
            if cell["source"] and cell["cell_type"] == "markdown"
        ]
        if not nonempty_md_contents:
            return None
        last_nonempty_md_content = nonempty_md_contents[-1].strip()
        if last_nonempty_md_content.lower().startswith("# conclusion"):
            conclusion = last_nonempty_md_content[len("# conclusion") :].strip()
            return conclusion
        else:
            return None

    @property
    def finished(self) -> bool:
        return self.conclusion is not None
