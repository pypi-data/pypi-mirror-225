from insight_plugin import VERSION
import sys
from insight_plugin.features.create.controller import CreateController
from insight_plugin.features.validate.controller import ValidateController
from insight_plugin.features.refresh.controller import RefreshController
from insight_plugin.features.run.run_controller import RunController
from insight_plugin.features.export.controller import ExportController
from typing import Tuple, Optional, Union
from insight_plugin.constants import (
    CREATE_DESCRIPTION,
    REFRESH_DESCRIPTION,
    RUN_DESCRIPTION,
    EXPORT_DESCRIPTION,
    VALIDATE_DESCRIPTION,
)
from insight_plugin.features.interactive.util.util import (
    retrieve_bool_input,
    retrieve_path_input,
    retrieve_jq_input,
    create_and_refresh_cli_controller,
    export_cli_controller,
    run_cli_controller,
    validate_cli_controller,
)


class _Option(object):
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description


# TODO: Make this dynamic instead of hardcoded
_OPTIONS = [
    # 1
    _Option(title="Create", description=CREATE_DESCRIPTION),
    # 2
    _Option(title="Refresh", description=REFRESH_DESCRIPTION),
    # 3
    _Option(title="Run", description=RUN_DESCRIPTION),
    # 4
    _Option(title="Validate", description=VALIDATE_DESCRIPTION),
    # 5
    _Option(title="Export", description=EXPORT_DESCRIPTION),
]


class InteractiveController(object):
    @staticmethod
    def prompt_menu():
        """
        This function handles the main functionality of printing
        the menu and retrieving the user input
        :return:
        """
        print(InteractiveController._get_interactive_menu_text())

        selection = None
        try:
            selection = int(input())
        except ValueError:
            sys.exit(1)

        InteractiveController._route_selection(selection=selection)

    @staticmethod
    def _route_selection(selection: int):
        """
        Handles the routing based on the user input
        :param selection: The users selection.
        :return:
        """
        if selection == 1:
            (
                path_to_spec,
                target_dir,
                verbose,
            ) = InteractiveController._get_create_refresh_controller_menu()

            controller = create_and_refresh_cli_controller(
                controller_name=CreateController,
                path_to_spec=path_to_spec,
                verbose=verbose,
                target_dir=target_dir,
            )
            controller.create()

        if selection == 2:
            (
                path_to_spec,
                target_dir,
                verbose,
            ) = InteractiveController._get_create_refresh_controller_menu()

            controller = create_and_refresh_cli_controller(
                controller_name=RefreshController,
                path_to_spec=path_to_spec,
                verbose=verbose,
                target_dir=target_dir,
            )

            controller.refresh()

        if selection == 3:
            (
                json_target,
                target_dir,
                verbose,
                assessment,
                is_test,
                jq,
            ) = InteractiveController._get_run_controller_menu()

            controller = run_cli_controller(
                controller_name=RunController,
                verbose=verbose,
                target_dir=target_dir,
                assessment=assessment,
                test=is_test,
                jq=jq,
                json_files=json_target,
            )

            controller.run()

        if selection == 4:
            path_to_spec = InteractiveController._get_validate_controller_menu()

            controller = validate_cli_controller(
                controller_name=ValidateController, path_to_spec=path_to_spec
            )

            controller.validate()

        if selection == 5:
            (
                no_pull,
                verbose,
                target_dir,
            ) = InteractiveController._get_export_controller_menu()

            controller = export_cli_controller(
                controller_name=ExportController,
                target_dir=target_dir,
                no_pull=no_pull,
                verbose=verbose,
            )

            controller.export()

        else:
            sys.exit(1)

    @staticmethod
    def _get_interactive_menu_text() -> str:
        """
        This method generates the initial interactive menu text.
        It produces a welcome statement and iterates through all
        potential options for the user.
        :return: The welcome menu
        :rtype: str
        """
        menu = f"Welcome to insight-plugin {VERSION}!\n\nWhat would you like to do?\n"

        for num, option in enumerate(_OPTIONS, start=1):
            menu += f"{num}. [{option.title}] - {option.description}\n"

        menu += "\nChoose a menu item from above or press any other key to exit: "

        return menu

    @staticmethod
    def _get_create_refresh_controller_menu() -> Tuple[str, Union[str, None], bool]:
        """
        A function to prompt the user to provide a path to the plugin spec
        file, target directory & verbose for the create & refresh subcommand.
        :return: Tuple containing path to spec file, target directory & verbose boolean.
        """

        # Handle path to spec file input
        path_to_spec = retrieve_path_input("plugin.spec.yaml")

        # Handle target directory input
        target_dir = retrieve_path_input("target directory")

        # Handle verbose input
        verbose = retrieve_bool_input("verbose")

        return path_to_spec, target_dir, verbose

    @staticmethod
    def _get_validate_controller_menu() -> str:
        """
        Method to handle inputs for the validate command.
        :return: Path to the plugin.spec.yaml file
        """

        # Handle path to spec file input
        path_to_spec = retrieve_path_input("plugin.spec.yaml")

        return path_to_spec

    @staticmethod
    def _get_run_controller_menu() -> Tuple[
        str,
        Union[str, None],
        bool,
        bool,
        bool,
        Optional[str],
    ]:

        """
        Method to handle the run subcommand inputs.
        :return: User inputs for verbose, target_dir, assessment, is_test, jq & json_target
        """

        # Handle json_files input
        json_target = retrieve_path_input("json_files")

        # Handle target directory input
        target_dir = retrieve_path_input("target directory")

        # Handle verbose input
        verbose = retrieve_bool_input("verbose")

        # Handle assessment input
        assessment = retrieve_bool_input("assessment")

        # Handle is_test input
        is_test = retrieve_bool_input("is_test")

        # Handle jq input
        jq = retrieve_jq_input(switch=retrieve_bool_input("jq"))

        return json_target, target_dir, verbose, assessment, is_test, jq

    @staticmethod
    def _get_export_controller_menu() -> Tuple[bool, bool, Union[str, None]]:
        """
        Method to handle the export subcommand inputs.
        :return: User inputs for no_pull, verbose & target directory
        """

        # Handle target directory input
        target_dir = retrieve_path_input("target directory")

        # Handle verbose input
        verbose = retrieve_bool_input("verbose")

        # Handle no pull input
        no_pull = retrieve_bool_input("--no-pull")

        return no_pull, verbose, target_dir
