import os
import sys
from unittest import TestCase

import ruamel.yaml

from insight_plugin.features.common.plugin_spec_util import PluginSpecUtil
from insight_plugin.features.version.controller import VersionController
from tests import TEST_RESOURCES

sys.path.append("../")

new_yaml = ruamel.yaml.YAML()


class TestSemver(TestCase):
    # Root directory for the test plugin
    target_dir = os.path.abspath(f"{TEST_RESOURCES}/semver_tests/base64")
    version_num = "1.1.7"
    spec_dict = PluginSpecUtil.get_spec_file(target_dir)

    def test_semver_function(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/test_base64/base64", version_num="1.1.8"
        )
        response = version_feature.semver()
        self.assertEqual(None, response)

    def test_spec_not_found(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/run_tests/run_test_base64"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
        self.assertTrue("plugin.spec not found" in str(context.exception))

    def test_error_handling_for_lesser_version(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/semver_tests/base64", version_num="1.1.5"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
        self.assertTrue(
            "New version must not be less than current version."
            in str(context.exception)
        )

    def test_error_handling_for_equal_version(self):
        version_feature = VersionController.new_from_cli(
            target_dir=f"{TEST_RESOURCES}/semver_tests/base64", version_num="1.1.6"
        )
        with self.assertRaises(Exception) as context:
            version_feature.semver()
            self.assertTrue(
                "New version must not match current version." in str(context.exception)
            )

    def test_update_yaml(self):
        VersionController._update_yaml_file(
            target_dir=self.target_dir, version_num=self.version_num
        )

        with open(os.path.join(self.target_dir, "plugin.spec.yaml"), "r") as file:
            data = new_yaml.load(file)
            data_version = data["version"]
        self.assertEqual(self.version_num, data_version)
