#!/usr/bin/env python3
import argparse
import logging

from argparse import Namespace

from insight_plugin import VERSION

from insight_plugin.features.create.controller import CreateController
from insight_plugin.features.samples.controller import GenSampleController
from insight_plugin.features.export.controller import ExportController
from insight_plugin.features.refresh.controller import RefreshController
from insight_plugin.features.run.run_controller import RunController
from insight_plugin.features.validate.controller import ValidateController
from insight_plugin.features.run.server_controller import RunServerController
from insight_plugin.features.run.bash_controller import RunShellController
from insight_plugin.features.interactive.controller import InteractiveController
from insight_plugin.features.common.exceptions import InsightException
from insight_plugin.features.version.controller import VersionController
from insight_plugin.features.view.controller import ViewController
from typing import List

DEFAULT_JQ_STRING = ".body.output"


def main():
    argparser = argparse.ArgumentParser(
        prog="insight-plugin",
        epilog=f"Version {VERSION}",
        description="Command-line tool to help develop plugins for the Rapid7 Insight Platform",
    )

    subparsers = argparser.add_subparsers(help="Commands")
    parsers_list = []

    # Create
    create_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Export
    export_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Refresh
    refresh_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Validate
    validate_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Semantic version
    semver_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Gen Samples
    samples_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Run
    run_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Run Docker Container as http server
    run_server_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Run Docker Container Bash
    run_shell_argparse(subparsers=subparsers, parsers_list=parsers_list)
    # Run docker info command
    view_argparse(subparsers=subparsers, parsers_list=parsers_list)

    # This adds arguments as an optional argument for all parsers(commands)
    for parser in parsers_list:
        # TODO - Do we need to add action="store_const" here?
        parser.add_argument(
            "-d", "--target-dir", help="Provide plugin directory", dest="target_dir"
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="Verbose Mode",
            action="store_true",
            dest="verbose",
        )

    argparser.add_argument(
        "--version",
        help="Show application version",
        dest="version",
        action="store_true",
    )

    args = argparser.parse_args()

    if args.version:
        print(VERSION)
    else:
        # If an argument was given then execute that. If arguments fail, fall back to interactive session
        try:
            args.func(args)
        except InsightException as error:
            logging.exception(error)
        except AttributeError:
            interactive()


def create_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the create subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_create = subparsers.add_parser("create", help=CreateController.HELP_MSG)
    command_create.add_argument(
        "spec_path",
        nargs="?",
        help="Path to the plugin.spec.yaml to generate a new plugin from",
    )
    parsers_list.append(command_create)
    command_create.set_defaults(func=create)


def create(args: Namespace) -> None:
    """
    Create a new insight plugin
    :param args: CLI args
    :return: None
    """
    controller = CreateController.new_from_cli(
        **{
            "spec_path": args.spec_path,
            "verbose": args.verbose,
            "target_dir": args.target_dir,
        }
    )
    if args.spec_path:
        controller.create()
    else:
        raise InsightException(
            message="No plugin.spec.yaml file found in path.",
            troubleshooting="Please provide a valid path to the plugin.spec.yaml file.",
        )


def export_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the export subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_export = subparsers.add_parser("export", help=ExportController.HELP_MSG)
    command_export.add_argument(
        "--no-pull",
        help="Flag to skip pulling the latest SDK base image during plugin export",
        dest="no_pull",
        action="store_true",
    )
    parsers_list.append(command_export)
    command_export.set_defaults(func=export)


def export(args: Namespace) -> None:
    """
    Run the export subcommand
    :param args: CLI args
    :return: None
    """
    controller = ExportController.new_from_cli(
        **{
            "no_pull": args.no_pull,
            "verbose": args.verbose,
            "target_dir": args.target_dir,
        }
    )
    controller.export()


def interactive() -> None:
    """
    Start a general interactive session with the user
    :return: None
    """
    InteractiveController.prompt_menu()


def refresh_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the refresh subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_refresh = subparsers.add_parser("refresh", help=RefreshController.HELP_MSG)
    command_refresh.add_argument(
        "spec_path",
        nargs="?",
        help="Path to the plugin.spec.yaml to refresh the plugin from",
    )
    parsers_list.append(command_refresh)
    command_refresh.set_defaults(func=refresh)


def refresh(args: Namespace) -> None:
    """
    Refresh the plugin MD5 checksums
    :param args: CLI args
    :return: None
    """
    controller = RefreshController.new_from_cli(
        spec_path=args.spec_path,
        verbose=args.verbose,
        target_dir=args.target_dir,
    )
    controller.refresh()


def run_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the run subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    # Add run command
    command_run = subparsers.add_parser("run", help=RunController.HELP_MSG)

    # Add .json_files positional argument
    command_run.add_argument(
        "json_target", type=str, nargs="?", help=".json files to run"
    )
    # Add assessment flag
    command_run.add_argument(
        "-A",
        "--assessment",
        help="Flag to generate plugin PR template output for contributions",
        dest="assessment",
        action="store_true",
    )
    # Add test flag
    command_run.add_argument(
        "-T",
        "--test",
        help="Run connection test. Uses first json file passed, or first in tests directory.",
        dest="is_test",
        action="store_true",
    )
    # Add JQ parser flag
    command_run.add_argument(
        "-J",
        "--jq",
        help=f"JQ Parser. Pass no args to use default ({DEFAULT_JQ_STRING}), or pass one used for all test/runs.",
        dest="jq",
        nargs="?",
        const=DEFAULT_JQ_STRING,
    )
    # Add rebuild flag
    command_run.add_argument(
        "-R",
        "--rebuild",
        help="Rebuild the Docker image before running it in a container and entering the shell",
        dest="rebuild",
        action="store_true",
    )
    # Add volume flag
    command_run.add_argument(
        "-V",
        "--volumes",
        type=str,
        nargs="+",
        help="Volume to mount from local machine to container, e.g. /Absolute/src:/Absolute/dest",
        dest="volumes",
    )

    parsers_list.append(command_run)
    command_run.set_defaults(func=run)


def run(args: Namespace) -> None:
    """
    Run the run subcommand
    :param args: CLI args
    :return: None
    """
    controller = RunController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
            "rebuild": args.rebuild,
            "assessment": args.assessment,
            "is_test": args.is_test,
            "jq_": args.jq,
            "json_target": args.json_target,
            "volumes": args.volumes,
        }
    )
    controller.run()


def run_shell_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the run_shell subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_run_bash = subparsers.add_parser("shell", help=RunShellController.HELP_MSG)
    parsers_list.append(command_run_bash)
    command_run_bash.set_defaults(func=run_shell)
    command_run_bash.add_argument(
        "-R",
        "--rebuild",
        help="Rebuild the Docker image before running it in a container and entering the shell",
        dest="rebuild",
        action="store_true",
    )

    command_run_bash.add_argument(
        "-V",
        "--volume",
        type=str,
        nargs="+",
        help="Volume to mount from local machine to container, e.g. /Absolute/src:/Absolute/dest",
        dest="volumes",
    )


def run_shell(args: Namespace) -> None:
    """
    Run the run_shell subcommand
    :param args: CLI args
    :return: None
    """
    controller = RunShellController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
            "volumes": args.volumes,
            "rebuild": args.rebuild,
        }
    )
    controller.run()


def run_server_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the run_server subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    # Add server command
    command_run_server = subparsers.add_parser(
        "server", help=RunServerController.HELP_MSG
    )
    # Add rebuild flag
    command_run_server.add_argument(
        "-m",
        "--rebuild",
        help="Rebuild the Docker image before running it in a container and entering the shell",
        dest="rebuild",
        action="store_true",
    )
    # Add port flag
    command_run_server.add_argument(
        "-p",
        "--port",
        type=str,
        nargs="+",
        default=["10001:10001"],
        help="List of ports to expose to other containers and scripts, for example 80:8080",
        dest="ports",
    )
    # Add volume flag
    command_run_server.add_argument(
        "-V",
        "--volume",
        type=str,
        nargs="+",
        help="Volume to mount from local machine to container, e.g. /Absolute/src:/Absolute/dest",
        dest="volumes",
    )
    parsers_list.append(command_run_server)
    command_run_server.set_defaults(func=run_server)


def run_server(args: Namespace) -> None:
    """
    Run the run_server subcommand
    :param args: CLI args
    :return: None
    """
    controller = RunServerController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
            "ports": args.ports,
            "volumes": args.volumes,
            "rebuild": args.rebuild,
        }
    )
    controller.run()


def samples_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the create samples subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_gen_samples = subparsers.add_parser(
        "samples", help=GenSampleController.HELP_MSG
    )

    command_gen_samples.add_argument(
        "target_component",
        nargs="?",
        help="Action/Trigger name to make samples for",
        type=str,
    )
    parsers_list.append(command_gen_samples)
    command_gen_samples.set_defaults(func=samples)


def samples(args: Namespace) -> None:
    """
    Generate the samples to test plugin actions/triggers
    :param args: CLI args
    :return: None
    """
    controller = GenSampleController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
            "target_component": args.target_component,
        }
    )

    controller.samples()


def semver_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle arg-parsing for semantic version subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_semver = subparsers.add_parser("semver", help=VersionController.HELP_MSG)
    command_semver.add_argument(
        "version_num",
        type=str,
        help="Format: X.X.X",
    )
    parsers_list.append(command_semver)
    command_semver.set_defaults(func=semver)


def semver(args: Namespace) -> None:
    """
    Run the semantic version command
    :param args: CLI args
    :return: None
    """
    controller = VersionController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
            "version_num": args.version_num,
        }
    )
    controller.semver()


def validate_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle arg-parsing for validate subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_validate = subparsers.add_parser(
        "validate", help=ValidateController.HELP_MSG
    )
    command_validate.add_argument(
        "spec_path",
        nargs="?",
        help="Path to the plugin.spec.yaml to be validated.",
        default=".",
    )
    parsers_list.append(command_validate)
    command_validate.set_defaults(func=validate)


def validate(args: Namespace) -> None:
    """
    Validate insight plugin
    :param args: CLI args
    :return: None
    """
    controller = ValidateController.new_from_cli(**{"spec_path": args.spec_path})
    controller.validate()


def view_argparse(subparsers, parsers_list: List) -> None:
    """
    Handle the arg-parsing for the view subcommand
    :param subparsers: List to be filled with commands
    :param parsers_list: List to be appended with parsed commands
    :return: None
    """
    command_view = subparsers.add_parser("view", help=ViewController.HELP_MSG)
    parsers_list.append(command_view)
    command_view.set_defaults(func=view)


def view(args: Namespace) -> None:
    """
    Run the view subcommand
    :param args: CLI args
    :return: None
    """
    controller = ViewController.new_from_cli(
        **{
            "verbose": args.verbose,
            "target_dir": args.target_dir,
        }
    )
    controller.run()


if __name__ == "__main__":
    main()
