import argparse
import os

from datasci_agents.cli import CLI


def valid_path(value):
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(f"Invalid path: {value}")
    return value


def main():
    parser = argparse.ArgumentParser(description="DataSci Agents CLI")
    parser.add_argument(
        "config_path", type=valid_path, help="Path to project configuration file."
    )

    args = parser.parse_args()
    config_path = args.config_path
    cli = CLI(config_path)
    cli.run()


if __name__ == "__main__":
    main()
