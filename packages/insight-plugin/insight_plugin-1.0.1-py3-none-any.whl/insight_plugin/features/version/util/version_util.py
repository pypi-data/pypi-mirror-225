from typing import Optional
import os
from insight_plugin.features.common.plugin_spec_util import (
    PluginSpecUtil,
)
from insight_plugin.features.create.util import (
    create_setup_py,
    create_manifest,
    create_checksum,
    get_prefix,
)
from insight_plugin.features.common.logging_util import BaseLoggingFeature
from insight_plugin.features.version.util.helpmd_util import HelpMdUtil
from insight_plugin.features.version.util.input_util import InputUtil
from insight_plugin.features.version.util.yaml_util import YamlUtil


class VersionUtil(BaseLoggingFeature):
    def __init__(
        self,
        version_num: Optional[str],
        verbose: bool,
        target_dir: str,
    ):

        super().__init__(verbose=verbose)
        self.version_num = version_num
        self.target_dir = os.path.abspath(target_dir)
        self.HelpMdUtil = HelpMdUtil(verbose, self.version_num, self.target_dir)
        self.InputUtil = InputUtil(verbose, self.version_num, self.target_dir)
        self.YamlUtil = YamlUtil(verbose, self.version_num, self.target_dir)

    def run(self):
        # TODO - Add additional positional argument to add string change
        # Error handling for input
        self.InputUtil.run()

        # Update the yaml file with the new version
        self.YamlUtil.run()

        # Update version number across relevant files
        self._update_files()

        # Add new line to help.md
        self.HelpMdUtil.run()

        print(f"Semver process complete!\nNew plugin version: {self.version_num}")

    def _update_files(self):
        """
        Helper function to run the methods to update:
        bin/{plugin} | .CHECKSUM | setup.py
        :param target_dir: The current plugin directory
        :param spec: The spec dictionary
        :return:
        """
        self.logger.info("Updating version number across plugin files..")

        spec = PluginSpecUtil.get_spec_file(self.target_dir)
        prefix = get_prefix(spec=spec, target_dir_name=self.target_dir)

        # bin/file.py
        create_manifest(spec=spec, bin_dir_name=self.target_dir)

        # .checksum
        create_checksum(spec=spec, target_dir_name=self.target_dir)

        # setup.py
        create_setup_py(spec=spec, target_dir_name=self.target_dir, prefix=prefix)
