import shutil
import tempfile
import unittest
from os.path import join
from typing import List

from insight_plugin.features.samples.controller import GenSampleController
from tests import TEST_RESOURCES
from tests import util


class TestSamples(unittest.TestCase):
    def test_major_plugin_types(self):
        plugins = {"test_base64", "test_carbon_black", "test_jira"}
        for plugin in plugins:
            mismatches = TestSamplesUtil.test_samples(plugin, False, "")
            if mismatches:
                for mismatch in mismatches:
                    print(mismatch)
                self.fail()

    def test_single_action_sample(self):
        mismatches = TestSamplesUtil.test_samples("single_sample_action", True, "assign_issue")
        if mismatches:
            for mismatch in mismatches:
                print(mismatch)
            self.fail()

    def test_single_trigger_sample(self):
        mismatches = TestSamplesUtil.test_samples("single_sample_trigger", True, "monitor_issues")
        if mismatches:
            for mismatch in mismatches:
                print(mismatch)
            self.fail()


class TestSamplesUtil:
    @staticmethod
    def test_samples(plugin_dir: str, is_single: bool, component: str) -> List[str]:
        # Examples of correctly created plugins exist under the tests/resources path
        test_dir = join(TEST_RESOURCES, plugin_dir)
        expect_dir = join(test_dir, "tests")

        # We create a temporary directory for the resulting content created by the test subject
        spec = join(test_dir, "plugin.spec.yaml")
        with tempfile.TemporaryDirectory() as temp_dir:
            shutil.copy(spec, temp_dir)
            sample_controller = GenSampleController.new_from_cli(
                verbose=True,
                target_dir=temp_dir,
                single=is_single,
                target_component=component,
            )
            # This method is the test subject!
            sample_controller.samples()

            result_dir = join(temp_dir, "tests")
            return util.compare_dir_contents(expect_dir, result_dir)
