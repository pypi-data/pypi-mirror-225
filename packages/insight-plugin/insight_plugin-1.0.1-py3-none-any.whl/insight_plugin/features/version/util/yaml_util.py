import os
from insight_plugin.features.common.logging_util import BaseLoggingFeature
from insight_plugin import FILE_ENCODING
import ruamel.yaml

yaml = ruamel.yaml.YAML()


class YamlUtil(BaseLoggingFeature):
    def __init__(self, verbose: bool, version_num: str, target_dir: str):

        super().__init__(verbose=verbose)
        self.version_num = version_num
        self.target_dir = target_dir

    def run(self):
        """
        Main run function
        :return:
        """
        # Update version tag
        self._update_yaml_version_tag()

    def _read_yaml(self):
        """
        Helper function to read yaml file
        :return:
        """
        self.logger.info("Reading yaml...")

        with open(
            os.path.join(self.target_dir, "plugin.spec.yaml"),
            "r+",
            encoding=FILE_ENCODING,
        ) as spec_file:
            yaml_data = yaml.load(spec_file)

        return yaml_data

    def _write_to_yaml(self, yaml_data):
        """
        Helper function to write yaml data to file.
        :param yaml_data: Yaml data to write
        :return:
        """
        self.logger.info("Writing to yaml...")

        with open(
            os.path.join(self.target_dir, "plugin.spec.yaml"),
            "w",
            encoding=FILE_ENCODING,
        ) as spec_file:
            yaml.dump(yaml_data, spec_file)

        return spec_file

    def _update_yaml_version_tag(self):
        """
        Helper function to append new version number to version tag in yaml file
        If not found, insert it somewhere around the start (index=4)
        :return:
        """
        self.logger.debug("Updating 'version' tag in yaml...")

        yaml_data = self._read_yaml()

        try:
            yaml_data["version"] = self.version_num
        except KeyError:
            yaml_data.insert(4, "version", self.version_num)

        self._write_to_yaml(yaml_data=yaml_data)
