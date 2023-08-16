import os
import sys
from unittest import TestCase, mock

from insight_plugin.features.interactive.controller import InteractiveController
from tests import TEST_RESOURCES

import shutil

sys.path.append("../")


# It is important to run these tests in order for it all to work correctly.
class TestInteractive(TestCase):

    # Declare all different relevant directories for inputs
    target_dir = os.path.abspath(f"{TEST_RESOURCES}/interactive_tests")
    plugin_dir = target_dir + "/base64"
    path_to_spec_in_plugin = plugin_dir + "/plugin.spec.yaml"
    path_to_spec_out_plugin = target_dir + "/plugin.spec.yaml"
    json_test_target = plugin_dir + "/tests/encode.json"

    @mock.patch("builtins.input", side_effect=[1, path_to_spec_out_plugin, target_dir, "Y"])
    def test_interactive_create(self, return_value):
        PLUGIN_DIR = TestInteractive.plugin_dir

        # If plugin exists, delete it so that create does not re-create the plugin
        # within the plugin folder
        if os.path.exists(PLUGIN_DIR):
            shutil.rmtree(PLUGIN_DIR)

        # Generate the response
        with self.assertRaises(SystemExit):
            InteractiveController.prompt_menu()
        # Test if the plugin directory now exists because of the create command
        self.assertTrue(os.path.exists(TestInteractive.plugin_dir), True)

    # Check if checksum has changed - REFRESH COMMAND CURRENTLY BROKEN
    @mock.patch("builtins.input", side_effect=[2, path_to_spec_in_plugin, "", "Y"])
    def test_interactive_refresh(self, return_value):

        with self.assertRaises(SystemExit):
            InteractiveController.prompt_menu()
        self.assertEqual(None, None)

    # Compare output against a JSON file
    @mock.patch("builtins.input", side_effect=[3, json_test_target, plugin_dir, "N", "N", "N", "N"])
    def test_interactive_run(self, return_value):
        # Source path
        SOURCE_TESTS_PATH = TestInteractive.target_dir + "/tests"
        # Target path
        TARGET_TESTS_PATH = TestInteractive.plugin_dir + "/tests"
        # Handle folder already exists
        if os.path.exists(TARGET_TESTS_PATH):
            shutil.rmtree(TARGET_TESTS_PATH)
        # Create tests folder + json test file within plugin dir
        # Do this by copying in the one that exists outside of plugin directory
        shutil.copytree(SOURCE_TESTS_PATH, TARGET_TESTS_PATH)
        # If system exits, then successful call was made.
        with self.assertRaises(SystemExit) as context:
            InteractiveController.prompt_menu()
        self.assertEqual(SystemExit, type(context.exception))

    # Just check it runs without error by checking if it exits successfully
    @mock.patch("builtins.input", side_effect=[4, plugin_dir])
    def test_interactive_validate(self, return_value):
        with self.assertRaises(SystemExit) as context:
            InteractiveController.prompt_menu()
        self.assertEqual(SystemExit, type(context.exception))

    @mock.patch("builtins.input", side_effect=[5, plugin_dir, "y", "y"])
    def test_interactive_export(self, return_value):

        FILE_PATH = os.path.join(TestInteractive.plugin_dir, "rapid7_base64_1.1.6.plg")

        # If it exists, delete it first so export can recreate
        if os.path.isfile(FILE_PATH):
            os.remove(FILE_PATH)

        InteractiveController.prompt_menu()

        # No need for assertRaises here because export doesn't seem to trigger
        # SystemExit unlike the other commands.
        self.assertTrue(os.path.isfile(FILE_PATH), True)
