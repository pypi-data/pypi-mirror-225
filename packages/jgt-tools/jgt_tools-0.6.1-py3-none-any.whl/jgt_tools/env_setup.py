"""
Setup the development environment.

Runs the following commands:
    {}
"""
import argparse
import os

from .utils import execute_command_list, CONFIGS, DEFAULT_CONFIGS

__commands_to_run = CONFIGS["env_setup_commands"]

__doc__ = __doc__.format("\n    ".join(__commands_to_run))


def env_setup(verbose):
    """Prepare environment for running."""
    print("In: {}".format(os.getcwd()))
    if os.getenv("VIRTUAL_ENV"):
        print(f"Setting up Virtual Environment: {os.environ['VIRTUAL_ENV']}")
    print()
    # In order to keep the initial install as lean as possible, the base installer only
    # install the libraries that are needed to run the library itself and all other
    # libraries are marked as optional. For a user to user the default commands,
    # additional libraries are needed and so this check first sees if the end user has
    # *not* modified the default command(s) and if the commands are the default ones,
    # install those libraries needed by the command. This intentionally cycles over
    # each command independently in case some are modified and some are not.
    for command in ("build_docs", "run_tests", "env_setup"):
        if DEFAULT_CONFIGS[f"{command}_commands"] == CONFIGS[f"{command}_commands"]:
            __commands_to_run.insert(2, f"poetry run pip install jgt_tools[{command}]")
    execute_command_list(__commands_to_run)


def main():
    """Execute env_setup using command line args."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show each command before it is executed",
    )
    args = parser.parse_args()
    env_setup(args.verbose)
