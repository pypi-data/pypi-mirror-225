from insight_plugin.features.common.exceptions import InsightException
from typing import Union, Type
from insight_plugin.features.create.controller import CreateController
from insight_plugin.features.validate.controller import ValidateController
from insight_plugin.features.refresh.controller import RefreshController
from insight_plugin.features.run.run_controller import RunController
from insight_plugin.features.export.controller import ExportController


####################
# HELPER FUNCTIONS #
####################
def retrieve_bool_input(name: str) -> bool:
    """
    This method returns True or False from a user input.
    Y/y = True | N/n = False
    :param name: Name for the variable the user is inputting.
    :return: True or False
    """
    input_string = messages_for_inputs(name=name)
    bool_input = str(input(input_string).lower().strip())

    if bool_input not in ("y", "n"):
        raise InsightException(
            message="Invalid input.", troubleshooting="Input must be (y) or (n)"
        )

    return bool_input == "y"


def messages_for_inputs(name: str) -> str:
    """
    This method produces different menu options depending on
    the input required from the user
    :param name: Name of the input
    :return: Input string
    """
    input_string = ""

    if name == "verbose":
        input_string = (
            "\nWould you like to use (-v) flag for verbose/debugging mode? (y/n)\n"
        )
    elif name == "assessment":
        input_string = (
            "\nWould you like to use (-A) flag to generate plugin PR template output for contributions? "
            "(y/n)\n"
        )
    elif name == "is_test":
        input_string = (
            "\nWould you like to use (-T) flag to run a connection test? (y/n)\n"
        )

    elif name == "jq":
        input_string = "\nWould you like to use (-j) flag to run the JQ parser? (y/n)\n"

    elif name == "json_files":
        input_string = "\nInput the path to the .json test file you would like to run\n"

    elif name == "--no-pull":
        input_string = (
            "\nWould you like to use the (--no-pull) flag?\nThis flag skips pulling the latest SDK base "
            "image during plugin export. (y/n)\n "
        )

    elif name in ("target directory", "plugin.spec.yaml"):
        input_string = f"\nInput the full path to the {name}.\nPress Enter for your current directory / default.\n"

    return input_string


def retrieve_path_input(name: str) -> str:
    """
    This function manages path inputs and handles empty path inputs accordingly.
    :param name: Name of the path input
    :return: String containing path to file or directory
    """
    input_message = messages_for_inputs(name=name)
    path = str(input(input_message))

    # Handle empty target_dir input
    if name == "target directory":
        if path == "":
            path = None

    # Handle empty plugin.spec.yaml input
    if name == "plugin.spec.yaml":
        if path == "":
            path = "plugin.spec.yaml"

    # Handle empty json files input
    if name == "json_files":
        if path == "":
            raise InsightException(
                message="No path provided.",
                troubleshooting="Please provide a path to the JSON test file(s)",
            )

    # Handle empty plugin spec yaml input for validate
    # For current dir, validate path must be '.'
    if name == "validate_plugin_spec":
        if path == "":
            path = ".."

    return path


def retrieve_jq_input(switch: bool) -> Union[str, None]:
    """
    This function handles JQ input.
    :param name: Name of the input
    :param switch: Boolean value for whether input is selected or not
    :return:
    """
    DEFAULT_JQ_STRING = ".body.output"
    jq = None

    if switch:
        jq = str(
            input(
                f"JQ Parser, Pass no args to use default ({DEFAULT_JQ_STRING}), or pass one used for all test/runs."
            )
        )

    return jq


#######################
# CONTROLLER BUILDERS #
#######################
def create_and_refresh_cli_controller(
    controller_name: Type[Union[CreateController, RefreshController]],
    path_to_spec: str,
    verbose: bool,
    target_dir: Union[str, None],
):
    """
    This function creates a new controller for the create & refresh subcommands
    :param controller_name: Name of the controller
    :param path_to_spec: Path to the spec file
    :param verbose: Boolean value indicating whether to add --verbose tag
    :param target_dir: String or None value containing target directory
    :return: Controller with all inputs filled
    """
    controller = controller_name.new_from_cli(
        **{
            "spec_path": path_to_spec,
            "verbose": verbose,
            "target_dir": target_dir,
        }
    )

    return controller


def export_cli_controller(
    controller_name: Type[ExportController],
    target_dir: Union[str, None],
    no_pull: bool,
    verbose: bool,
):
    """
    This function creates a new controller for the export subcommand
    :param controller_name: Name of the controller
    :param target_dir: Path to the target directory
    :param no_pull: Boolean value indicating whether to add --no-pull tag
    :param verbose: Boolean value indicating whether to add --verbose tag
    :return: Controller with all inputs filled
    """
    controller = controller_name.new_from_cli(
        **{
            "no_pull": no_pull,
            "verbose": verbose,
            "target_dir": target_dir,
        }
    )

    return controller


def run_cli_controller(
    controller_name: Type[RunController],
    verbose: bool,
    target_dir: Union[str, None],
    assessment: bool,
    test: bool,
    jq: str,
    json_files: str,
):
    """
    This function creates a new controller for the run subcommand
    :param controller_name:  Name of the controller
    :param verbose: Boolean value indicating whether to add --verbose tag
    :param target_dir: Path to the target directory
    :param assessment: Boolean value indicating whether to add --assessment tag
    :param test: Boolean value indicating whether to add --is_test flag
    :param jq:
    :param json_files: Path to json files
    :return: Controller with all inputs filled
    """
    controller = controller_name.new_from_cli(
        **{
            "verbose": verbose,
            "target_dir": target_dir,
            "assessment": assessment,
            "is_test": test,
            "jq_": jq,
            "json_target": [json_files],
        }
    )

    return controller


def validate_cli_controller(
    controller_name: Type[ValidateController], path_to_spec: str
):
    """
    This function creates a new controller for the run subcommand
    :param controller_name: Name of the controller
    :param path_to_spec: Path to the plugin.spec.yaml
    :return: Controller with all inputs filled
    """

    controller = controller_name.new_from_cli(**{"spec_path": path_to_spec})

    return controller
