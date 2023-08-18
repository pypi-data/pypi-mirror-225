from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from datasci_agents.project import Project
from datasci_agents.experiment import Experiment
from datasci_agents.experiment_factory import ExperimentFactory
from datasci_agents.experiment_agent import ExperimentAgent

colorama_init()


welcome_message = f"""


{Fore.BLUE}\
    ============================================
    |||  Welcome to the DataSci Agents CLI!  |||
    ============================================


DataSci Agents are LLM-powered agents that help you create 
and run data science experiments.

All of the experiments are stored as Jupyter notebooks. 
Experiments are created automatically by the system, but you 
can create them manually manually as well: simply add a new 
notebook to the experiments folder and describe the experiment
goals in the first markdown cell.

To start, we will create a new experiment if no pending 
experiments are detected, or load an existing one. Then, our 
Experiment Agent will run the experiment step by step: you can 
track how it works in the notebook itself. If the agent has any 
questions, it will ask you! If you want to stop the agent, simply 
press Ctrl+C. Agents are happy to continue their work later.
{Style.RESET_ALL}

"""


class CLI:
    def __init__(
        self,
        config_path,
    ):
        self.project = Project(config_path)

    def run(self):
        print(welcome_message)
        while True:
            unfinished_experiments = self.project.unfinished_experiments
            if unfinished_experiments:
                next_experiment = self.ask_user_for_next_experiment(
                    unfinished_experiments
                )
                self.run_experiment(next_experiment)
            else:
                self.generate_new_experiment()

    def ask_user_for_next_experiment(self, experiments: list[Experiment]):
        assert len(experiments) > 0
        print(Fore.YELLOW)
        print(f"Pending experiments:")
        for i, experiment in enumerate(experiments):
            print(f"\t{i+1}. {experiment.name}")
        print(Style.RESET_ALL)
        next_experiment_idx = input(
            f"{Fore.GREEN}Select the experiment to run [1]: {Style.RESET_ALL}"
        )
        if not next_experiment_idx:
            next_experiment_idx = 1
        next_experiment_idx = int(next_experiment_idx) - 1
        next_experiment = experiments[next_experiment_idx]
        return next_experiment

    def run_experiment(self, experiment: Experiment):
        print(
            f"\n{Fore.YELLOW}Running experiment {experiment.name}...{Style.RESET_ALL}"
        )
        experiment_agent = ExperimentAgent(
            project=self.project,
            experiment=experiment,
        )
        for step_output in experiment_agent.loop():
            if step_output.message:
                color = Fore.RED if step_output.error else Fore.GREEN
                print(f"\n{color}{step_output.message}{Style.RESET_ALL}")
            if step_output.pause_loop:
                input(
                    f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}"
                )
            if step_output.restart_agent:
                experiment_agent.restart()

    def generate_new_experiment(self):
        while True:
            print(f"\n{Fore.YELLOW}Creating a new experiment...{Style.RESET_ALL}")
            experiment_factory = ExperimentFactory(
                project=self.project,
            )
            pending_experiment = experiment_factory.generate_pending_experiment()
            print(
                f"\n{Fore.YELLOW}Created experiment {pending_experiment.name}:\n"
                f"{pending_experiment.specification}{Style.RESET_ALL}"
            )
            approve = input(f"{Fore.GREEN}Approve experiment? [y/n]{Style.RESET_ALL}")
            if approve.lower().startswith("n"):
                continue
            break
        experiment = Experiment.from_pending_experiment(
            pending_experiment=pending_experiment,
            experiment_dir=self.project.experiments_path,
        )
        return experiment
