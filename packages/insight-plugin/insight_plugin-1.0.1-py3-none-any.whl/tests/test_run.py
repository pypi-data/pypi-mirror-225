import unittest

from insight_plugin.features.common.exceptions import (
    InsightException,
    RunCommandExceptions,
)
from insight_plugin.features.run.bash_controller import RunShellController
from insight_plugin.features.run.run_controller import RunController
from insight_plugin.features.run.util.run_util import RunCommand
from insight_plugin.features.run.server_controller import RunServerController
from tests import TEST_RESOURCES


class TestRun(unittest.TestCase):
    def test_run_invalid_json(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_controller = RunController.new_from_cli(
            verbose=True,
            target_dir=target_dir,
            assessment=False,
            is_test=False,
            json_target=["tests/invalid_file.json"],
        )
        with self.assertRaises(InsightException) as error:
            run_controller.run()
            self.assertEqual(
                error.exception.troubleshooting,
                RunCommandExceptions.TEST_FILE_INVALID_JSON_TROUBLESHOOTING,
            )

    def test_run_missing_type(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_controller = RunController.new_from_cli(
            verbose=True,
            target_dir=target_dir,
            assessment=False,
            is_test=False,
            json_target=["tests/decode_missing_type.json"],
        )
        with self.assertRaises(InsightException) as error:
            run_controller.run()
            self.assertEqual(
                error.exception.troubleshooting,
                RunCommandExceptions.JSON_TYPE_NOT_IN_JSON_TROUBLESHOOTING,
            )

    #
    def test_missing_json(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_controller = RunController.new_from_cli(
            verbose=False,
            target_dir=target_dir,
            assessment=False,
            is_test=False,
            json_target=["tests/decode_non_existent_file.json"],
        )
        with self.assertRaises(InsightException) as error:
            run_controller.run()
            self.assertEqual(
                error.troubleshooting,
                RunCommandExceptions.TEST_FILE_NOT_FOUND_TROUBLESHOOTING,
            )

    def test_run_missing_required_input(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_controller = RunController.new_from_cli(
            verbose=False,
            target_dir=target_dir,
            assessment=False,
            is_test=True,
            json_target=["tests/decode_missing_required.json"],
        )
        run_controller.run()
        run_controller.run_outputs[0].serialize_last_output()
        output = run_controller.run_outputs[0].output
        if (
            "Plugin step input contained a null value or empty string in a required input"
            not in output
        ):
            self.fail(f"Incorrect error message: {output}")

    def test_build_http_cmd(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_http_controller = RunServerController.new_from_cli(
            verbose=True,
            target_dir=target_dir,
            volumes=["/var/cache:/var/cache"],
            ports=["80:8080"],
        )
        cmd = " ".join(run_http_controller.build_command())
        self.assertEqual(
            cmd,
            "run --rm -p 80:8080 -v /var/cache:/var/cache rapid7/base64:1.1.6 http --debug",
        )

    def test_build_shell_cmd(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/run_test_base64/base64"
        run_shell_controller = RunShellController.new_from_cli(
            verbose=True, target_dir=target_dir, volumes=["/var/cache:/var/cache"]
        )
        cmd = " ".join(run_shell_controller.build_command("sh"))
        self.assertEqual(
            cmd,
            "run --rm --entrypoint sh -i -t -v /var/cache:/var/cache rapid7/base64:1.1.6 --debug",
        )

    def test_run_command_jq_success(self):
        full_cmd_sim_output = [
            "rapid7/Base64:1.1.6. Step name: decode",
            '{"body": { "log": "rapid7/Base64:1.1.6. Step name: decode\\n", "status": "ok", "meta": {}, "output": { "data": "superencode"}}, "version": "v1", "type": "action_event"}',
        ]

        run_command = RunCommand(
            command_run="docker run --rm -i rapid7/base64:1.1.6 run < tests/decode.json",
            full_output=full_cmd_sim_output,
        )
        run_command.serialize_last_output()
        self.assertEqual(
            run_command.jq_output(".body.output"), [{"data": "superencode"}]
        )

    def test_run_command_bad_jq(self):
        full_cmd_sim_output = [
            "rapid7/Base64:1.1.6. Step name: decode",
            '{"body": { "log": "rapid7/Base64:1.1.6. Step name: decode\\n", "status": "ok", "meta": {}, "output": { "data": "superencode"}}, "version": "v1", "type": "action_event"}',
        ]

        run_command = RunCommand(
            command_run="docker run --rm -i rapid7/base64:1.1.6 run < tests/decode.json",
            full_output=full_cmd_sim_output,
        )
        run_command.serialize_last_output()
        with self.assertRaises(InsightException) as e:
            run_command.jq_output(pattern=".{]BAD_+=")
        self.assertEqual(
            e.exception.troubleshooting,
            RunCommandExceptions.JQ_COMPILE_FAIL_TROUBLESHOOTING,
        )

    def test_run_all(self):
        target_dir = f"{TEST_RESOURCES}/run_tests/normal_base64"
        run_controller = RunController.new_from_cli(
            verbose=True,
            target_dir=target_dir,
            assessment=True,
            is_test=True,
            volumes=["/var/cache:/var/cache"],
            json_target=None,
        )
        run_controller.run()

    # try to get the coverage % for this command
