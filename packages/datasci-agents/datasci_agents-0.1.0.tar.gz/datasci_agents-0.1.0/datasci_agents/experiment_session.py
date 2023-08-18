import os
from typing import Optional
from copy import deepcopy
import nbformat as nbf
from nbformat.notebooknode import NotebookNode
from jupyter_client.manager import KernelManager

from datasci_agents.experiment import Experiment


class ExperimentSession:
    def __init__(self, experiment: Experiment):
        self.experiment = deepcopy(experiment)  # TODO: let's try to avoid this

    def run(self) -> None:
        self.km = KernelManager(kernel_name="python3")
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()
        for cell in self.experiment.notebook.cells:
            if cell["cell_type"] == "code":
                outputs = self.execute_code(cell.source)
                cell["outputs"] = outputs

    def execute_code(self, code: str) -> list[NotebookNode]:
        # Execute with existing kernel client
        self.kc.execute(code)
        # Collect the outputs as they arrive
        outputs = []
        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=1)
                msg_type = msg["msg_type"]
                content = msg["content"]
                if msg_type == "stream":
                    outputs.append(
                        nbf.v4.new_output(
                            output_type="stream",
                            name=content["name"],
                            text=content["text"],
                        )
                    )
                elif msg_type == "error":
                    outputs.append(
                        nbf.v4.new_output(
                            output_type="error", traceback=content["traceback"]
                        )
                    )
                elif msg_type in ["display_data", "execute_result"]:
                    outputs.append(
                        nbf.v4.new_output(
                            output_type=msg_type,
                            data=content["data"],
                            metadata=content["metadata"],
                        )
                    )
            except Exception as e:
                break
        return outputs

    def execute_and_add_code_cell(self, code: str) -> list[NotebookNode]:
        # Execute the generated code
        outputs = self.execute_code(code)
        # Add the code and its output to the notebook
        self.experiment.add_code_cell(source=code, outputs=outputs)
        # Return the outputs
        return outputs

    def add_markdown_cell(self, source: str) -> None:
        self.experiment.add_markdown_cell(source=source)

    def reload(self) -> None:
        # TODO: add code cell conflict checks to prompt a rerun
        self.experiment.load_notebook()

    def save(self) -> None:
        # TODO: add conflict checks
        self.experiment.save_notebook()

    def close(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()
        del self.kc
        del self.km
