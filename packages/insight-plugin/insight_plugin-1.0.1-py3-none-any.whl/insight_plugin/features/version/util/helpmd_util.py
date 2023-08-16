import os
from insight_plugin.features.common.logging_util import BaseLoggingFeature
from insight_plugin import FILE_ENCODING


class HelpMdUtil(BaseLoggingFeature):
    def __init__(self, verbose, version_num, target_dir):
        super().__init__(verbose=verbose)
        self.version_num = version_num
        self.target_dir = target_dir

    def run(self):
        """
        A function to add a new line to the changelog in the help.md
        :return: An amended help.md
        """

        # Write new version to the raw_help string
        self.insert_new_version()

    def insert_new_version(self):
        """
        Add '* {version_num} - ' to changelog in help.md
        :return:
        """
        raw_help = self.read_help_md(target_dir=self.target_dir)

        # Get the start and end of the version history section
        version_history_pattern = raw_help.find("# Version History")
        links_pattern = raw_help.find("# Links")

        # Extract only the version history section
        version_history = raw_help[version_history_pattern:links_pattern]

        # Split the section into a list
        version_history_list = version_history.splitlines()

        # Insert the new version into the list
        version_history_list.insert(2, f"* {self.version_num} - ")

        # Convert list back to original string?
        new_version_history = "\n".join(version_history_list)

        new_help_md = (
            raw_help[:version_history_pattern]
            + new_version_history
            + raw_help[links_pattern:]
        )

        # Overwrite old file with new help string
        self.write_help_md(new_help_md)

    def read_help_md(self, target_dir: str) -> str:
        """
        Helper method to read help_md file and convert to string
        :param target_dir: Path to target directory containing help.md file
        :return: raw_help string
        """
        self.logger.info("Reading help.md")

        with open(
            os.path.join(target_dir + "/help.md"), "r", encoding=FILE_ENCODING
        ) as file:
            raw_help = file.read()

        return raw_help

    def write_help_md(self, help_md: str) -> str:
        """
        Helper method to write raw_help string to a .md file
        :param help_md: Raw help string
        :return: Help.md file
        """
        self.logger.info("Writing to help.md")

        with open(
            os.path.join(self.target_dir + "/help.md"), "w", encoding=FILE_ENCODING
        ) as file:
            file.write(help_md)

        return help_md
