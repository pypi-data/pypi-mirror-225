import unittest
from os.path import join

from parameterized import parameterized

from insight_plugin import BASE_PREFIX, FILE_ENCODING, KOMAND_PREFIX
from insight_plugin.features.common.checksum_util import ChecksumUtil
from insight_plugin.features.common.plugin_spec_util import (
    PluginSpecConstants,
    PluginSpecUtil,
)
from tests import TEST_RESOURCES


class TestChecksum(unittest.TestCase):
    def test_create_sum_from_file(self):
        input_file = join(TEST_RESOURCES, "export_test_base64", "extension.png")
        result = ChecksumUtil._create_sum_from_file(input_file)
        self.assertEqual(result, "e41a1513ef7eb7d68193d6f25ebadf12")

    @staticmethod
    def get_checksum(plugin_dir: str, prefix: str):
        plugin_spec_filename = join(plugin_dir, PluginSpecConstants.FILENAME)
        plugin_spec = PluginSpecUtil.get_spec_file(plugin_spec_filename)
        return ChecksumUtil.create_checksums(
            plugin_dir, plugin_spec, base_prefix=prefix
        )

    @staticmethod
    def get_expected(plugin_dir: str):
        with open(
            join(plugin_dir, ".CHECKSUM"), "r", encoding=FILE_ENCODING
        ) as expected_file:
            return expected_file.read()

    @parameterized.expand(
        [
            ("export_test_base64", KOMAND_PREFIX),
            ("test_carbon_black/carbon_black_defense", BASE_PREFIX),
        ]
    )
    def test_checksum_plugin(self, plugin_dir, prefix):
        plugin_dir = join(TEST_RESOURCES, plugin_dir)
        expected = TestChecksum.get_expected(plugin_dir)
        result = TestChecksum.get_checksum(plugin_dir, prefix)

        self.assertEqual(expected, result)
