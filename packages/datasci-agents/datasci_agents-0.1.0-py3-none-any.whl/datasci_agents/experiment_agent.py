import re
from typing import Optional
from typing import Generator

from datasci_agents.llm import llm_complete
from datasci_agents.project import Project
from datasci_agents.experiment import Experiment
from datasci_agents.experiment_session import ExperimentSession


class AgentStepOutput:
    def __init__(
        self,
        message: Optional[str] = None,
        experiment_finished: bool = False,
        error: bool = False,
        pause_loop: bool = False,
        restart_agent: bool = False,
    ):
        self.message = message
        self.experiment_finished = experiment_finished
        self.error = error
        self.pause_loop = pause_loop
        self.restart_agent = restart_agent


class ExperimentAgent:
    experiment_instructions_template = """\
{project_instructions}


== Current task ==

{experiment_specification}


== Instructions ==

You are working in a Jupyter notebook. You write code, and you get results back from the "user".
To write code, you need to send a message which includes a code block inside ```python ... ``` tags.
Work on the task step by step. Print out intermediate results to make sure you are on the right track. Wait for the output from Jupyter of each step, before proceeding.
Since you are not able to see the plots, use simple printouts of statistics every time it is possible.
If plots are needed (e.g. to spot trends or anomalies), plot them in the usual way and "user" will provide you a description of each plot. Treat this description as a normal output, and continue your work after it. If you are asked to visualize something, this description will be considered a successful visualization.
When finished, write a conclusion in a single message. Conclusion should answer the original question and be concise. Conclusion has to start with the header "# Conclusion".
"""

    plot_description_questions_message = """\
Since you are not able to see the plot, please list the questions about the plot important for this experiment and I will answer them. 
List the questions without writing anything else. Each question starts with "- ".'
"""

    # Pretending that description is some structured output, otherwise the model gets chatty
    plot_description_template = """\
[plot description missing]  (remove this line when you write the description)

<plot_description>

{description}

</plot_description>
"""

    def __init__(
        self,
        project: Project,
        experiment: Experiment,
    ):
        self.project = project
        config = self.project.get_agent_config("experiment_agent")
        self.llm_kwargs = config.get("llm", {})
        self.start_experiment_session(experiment=experiment)

    def start_experiment_session(self, experiment: Experiment) -> None:
        self.experiment_session = ExperimentSession(experiment=experiment)
        self.experiment_session.run()

    @property
    def experiment(self) -> Experiment:
        return self.experiment_session.experiment

    @property
    def experiment_instructions(self) -> str:
        experiment_instructions = self.experiment_instructions_template.format(
            project_instructions=self.project.instructions,
            experiment_specification=self.experiment.specification,
        )
        return experiment_instructions

    def step(self) -> AgentStepOutput:
        if self.experiment.finished:
            AgentStepOutput(
                message=f"Experiment is finished, with the following conclusion:\n\n {self.experiment.conclusion}",
                experiment_finished=True,
            )
        step_output = AgentStepOutput()
        messages = self.construct_messages()
        agent_response = llm_complete(messages=messages, **self.llm_kwargs)
        parsed_response = self.parse_agent_response(agent_response)
        response_type, response_content = (
            parsed_response["response_type"],
            parsed_response["content"],
        )
        if response_type == "code":
            outputs = self.experiment_session.execute_and_add_code_cell(
                response_content
            )
            error_outputs = [o for o in outputs if o["output_type"] == "error"]
            if error_outputs:
                step_output = AgentStepOutput(
                    message=f"Error ocurred in the {self.experiment.name} experiment. Please fix the error before continuing.",
                    error=True,
                    pause_loop=True,
                    restart_agent=True,
                )
            visual_outputs = [o for o in outputs if o["output_type"] == "display_data"]
            if visual_outputs:
                self.add_last_plot_description_prompt()
                step_output = AgentStepOutput(
                    message=f"Please describe the plot in the {self.experiment.name} experiment",
                    pause_loop=True,
                )
        elif response_type == "markdown":
            self.experiment_session.add_markdown_cell(response_content)
        self.experiment_session.save()
        return step_output

    def loop(self) -> Generator[AgentStepOutput, None, None]:
        while not self.experiment.finished:
            try:
                output = self.step()
                yield output
            except Exception as e:
                yield AgentStepOutput(
                    message=f"Error ocurred in the {self.experiment.name} experiment. Please fix the error before continuing.",
                    error=True,
                    pause_loop=True,
                    restart_agent=True,
                )

    def format_cell_outputs(self, outputs) -> str:
        # TODO: not too happy that nbformat specifics are leaking here
        formatted_outputs = []
        for output in outputs:
            output_type = output["output_type"]
            if output_type == "stream":
                formatted_outputs.append(output["text"])
            elif output_type == "error":
                formatted_outputs.append("\n".join(output["traceback"]))
            elif output_type == "execute_result":
                formatted_outputs.append(output["data"]["text/plain"])
        return "\n".join(formatted_outputs)

    def construct_messages(self):
        messages = [
            {"role": "system", "content": self.experiment_instructions},
        ]
        for cell in self.experiment.cells:
            cell_type = cell["cell_type"]
            cell_source = cell.get("source", "").strip()
            cell_outputs = cell.get("outputs", [])
            if not cell_source:
                continue
            if cell_type == "code":
                messages.append(
                    {"role": "assistant", "content": f"```python\n{cell_source}\n```"}
                )
            elif cell_type == "markdown":
                messages.append({"role": "assistant", "content": cell_source})
            if cell_outputs:
                output_str = self.format_cell_outputs(cell_outputs)
                messages.append({"role": "user", "content": output_str})
        return messages

    def parse_agent_response(self, agent_response) -> dict:
        # Search for ```python ... ``` and ``` ... ``` patterns
        pattern = r"```(?:python)?(.*?)```"
        matches = re.findall(pattern, agent_response, re.DOTALL)
        code_blocks = [match.strip() for match in matches]
        code = "\n\n".join(code_blocks)
        # TODO: maybe we want to add non-code text as comments (even though they're usually useless)?
        if code:
            return {"response_type": "code", "content": code}
        else:
            return {"response_type": "markdown", "content": agent_response}

    def add_last_plot_description_prompt(self):
        # ask LLM for questions
        messages = self.construct_messages()
        messages.append(
            {"role": "user", "content": self.plot_description_questions_message}
        )
        plot_description_questions = llm_complete(messages=messages, **self.llm_kwargs)

        # add MD cell with questions
        plot_description_questions_formatted = self.plot_description_template.format(
            description=plot_description_questions
        )
        self.experiment_session.add_markdown_cell(plot_description_questions_formatted)

    def experiment_has_missing_plot_descriptions(self):
        cells = self.experiment.cells
        for cell in cells:
            cell_type = cell["cell_type"]
            cell_source = cell.get("source", "").strip()
            if (
                cell_type == "markdown"
                and "[plot description missing]" in cell_source()
            ):
                return True
        return False

    def restart(self):
        self.close_session()
        self.start_experiment_session(experiment=self.experiment)

    def close_session(self):
        self.experiment_session.close()
