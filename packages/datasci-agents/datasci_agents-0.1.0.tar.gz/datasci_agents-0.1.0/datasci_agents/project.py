import os
import pandas as pd
import yaml

from datasci_agents.experiment import Experiment


# Force YAML to write text in multiline blocks
def yaml_multiline_string_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        data = "\n".join([line.rstrip() for line in data.strip().splitlines()])
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, yaml_multiline_string_presenter)


class Project:
    project_instructions_template = """\
You are a data scientist. Because data science is a science, your primary goal is not to win some competition, it is to ask meaningful questions and answer them. Winning is simply a side effect.
Your work is organized as follows:
- Project is initiated with project documentation and a dataset.
- Question to answer is defined, and the team runs an experiment to answer it.
- Results of the experiment are documented.
- Solution is revised based on the new knowledge. If a satisfying solution to the project is found, the project is completed. Otherwise, new question is created, and the project continues.


== Project documentation ==

{documentation}


== Data ==

{data}


== Experiment Findings ==

{experiments_description}


== Current solution outline ==

{current_solution}

"""

    def __init__(self, config_path):
        with open(config_path, "r") as f:
            config: dict = yaml.safe_load(f)
        self.home_path = os.path.dirname(config_path)
        self.experiments_path = os.path.join(self.home_path, "experiments")
        self.name = config.pop("name")
        self.dataset_config = config.pop("dataset")
        self.documentation = config.pop("documentation")
        self.agent_configs = config
        self.data_path = os.path.join(self.home_path, self.dataset_config["path"])
        self._dataset = None
        self._experiments = None
        self.current_solution = None  # TODO

    @property
    def dataset(self):
        # Lazy loading the dataset
        if self._dataset:
            return self._dataset
        self._dataset = {}
        for file in os.listdir(self.data_path):
            if (not file.startswith("_")) and file.endswith(".csv"):
                self._dataset[file.replace(".csv", "")] = pd.read_csv(
                    os.path.join(self.data_path, file)
                )
        return self._dataset

    def get_agent_config(self, agent) -> dict:
        return self.agent_configs.get(agent, {})

    @property
    def experiments(self) -> list[Experiment]:
        # Lazy loading the experiments
        if self._experiments:
            return self._experiments
        self._experiments = []
        for file in os.listdir(self.experiments_path):
            if (not file.startswith("_")) and file.endswith(".ipynb"):
                notebook_path = os.path.join(self.experiments_path, file)
                experiment = Experiment(notebook_path)
                self._experiments.append(experiment)
        return self._experiments

    @property
    def unfinished_experiments(self) -> list[Experiment]:
        return [
            experiment for experiment in self.experiments if not experiment.finished
        ]

    @property
    def data_description(self) -> str:
        description_lines = [
            f"Data is located in folder: `{self.data_path}` in csv files. Following files are available.\n"
        ]
        for name, df in self.dataset.items():
            description_lines.append(f"## {name}")
            description_lines.append(df.head(3).to_markdown())
            description_lines.append("")
        return "\n".join(description_lines)

    @property
    def experiments_description(self) -> str:
        conclusions = []
        for experiment in self.experiments:
            conclusion = experiment.conclusion
            if conclusion:
                conclusions.append(conclusion)
        if conclusions:
            return "\n\n".join(conclusions)
        else:
            return "<no experiments yet>"

    @property
    def instructions(self) -> str:
        return self.project_instructions_template.format(
            documentation=self.documentation,
            data=self.data_description,
            experiments_description=self.experiments_description,
            current_solution=self.current_solution or "<no solution yet>",
        )
