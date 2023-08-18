from datasci_agents.llm import llm_complete
from datasci_agents.project import Project
from datasci_agents.experiment import Experiment, PendingExperiment


class ExperimentFactory:
    generate_question_message = """\
Considering the goal of the project, the findings so far and the current solution (if they exist), suggest the next experiment to run.
Initial steps should revolve around EDA. Start slow and simple. When data is sufficiently explored, start with more complex questions about feature engineering, then modeling.
Each experiment is well defined, self contained, and can be answered with a single jupyter notebook.

Write your output as a JSON dictionary with the following fields:
{
    "question": "Detailed question the experiment should answer",
    "experiment_code": "snake_case, short, unique identifier of the experiment, to name the experiment notebook and other files/folders",
    "motivation": "Why is this question important and how would an answer to it help us going forward",
    "expected_answer": "What answer do we expect? if it is not possible to estimate, then explain what type of answer we expect - how does an answer look like?"
}

Do not write anything else, only this JSON dictionary.
"""

    def __init__(
        self,
        project: Project,
    ):
        self.project = project
        config = self.project.get_agent_config("question_agent")
        self.llm_kwargs = config.get("llm", {})
        self._last_question_agent = None

    def generate_pending_experiment(self) -> PendingExperiment:
        messages = [
            {"role": "system", "content": self.project.instructions},
            {"role": "user", "content": self.generate_question_message},
        ]
        specification_components = llm_complete(
            messages=messages,
            json_keys=["question", "experiment_code", "motivation", "expected_answer"],
            **self.llm_kwargs,
        )
        specification = self.format_specification(specification_components)
        name = specification_components["experiment_code"]
        pending_experiment = PendingExperiment(
            name=name,
            specification=specification,
        )
        return pending_experiment

    def generate_experiment(self) -> Experiment:
        pending_experiment = self.generate_pending_experiment()
        experiment = Experiment.from_pending_experiment(
            pending_experiment=pending_experiment,
            experiment_dir=self.project.experiments_path,
        )
        return experiment

    def format_specification(self, specification_components: dict):
        return (
            f"# Question\n{specification_components['question']}\n"
            f"\n## Motivation\n{specification_components['motivation']}\n"
            f"\n## Expected answer\n{specification_components['expected_answer']}\n"
        )
