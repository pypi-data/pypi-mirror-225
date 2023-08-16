import os
from insight_plugin.features.common.logging_util import BaseLoggingFeature
from insight_plugin.features.common.exceptions import InsightException
from insight_plugin.features.common.plugin_spec_util import (
    PluginSpecUtil,
)
import semver


class InputUtil(BaseLoggingFeature):
    def __init__(self, verbose: bool, version_num: str, target_dir: str):

        super().__init__(verbose=verbose)
        self.version_num = version_num
        self.target_dir = target_dir

    def run(self):
        """
        Run function
        :return:
        """
        # Check version positional argument
        self._check_version_argument()

        # Check target directory is real
        self._check_directory_argument()

    def _check_version_argument(self) -> None:
        """
        A function to check user input is greater than the current version.
        :param target_dir: Path to target directory
        :param version_num: The users inputted, new, version number
        :return:
        """
        self.logger.debug("Checking version argument")

        # Load spec file
        spec = PluginSpecUtil.get_spec_file(self.target_dir)
        # self.logger.debug(f"Spec: {spec}")

        # Retrieve the current spec version
        spec_version = spec.get("version")

        version_compare = semver.compare(spec_version, self.version_num)

        if version_compare == 0:
            raise InsightException(
                message="New version must not match current version.",
                troubleshooting="Check your version input and try again",
            )
        elif version_compare > 0:
            raise InsightException(
                message="New version must not be less than current version.",
                troubleshooting="Check your version input and try again.",
            )

    def _check_directory_argument(self) -> None:
        """

        :param target_dir:
        :return:
        """
        if not os.path.isfile(os.path.join(self.target_dir, "plugin.spec.yaml")):
            raise InsightException(
                message="plugin.spec not found",
                troubleshooting="Please ensure you are running the command from the plugin.spec directory",
            )
