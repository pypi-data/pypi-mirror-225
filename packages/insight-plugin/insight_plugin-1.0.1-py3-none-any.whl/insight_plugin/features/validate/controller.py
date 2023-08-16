from insight_plugin.features.common.common_feature import CommonFeature
from icon_validator.validate import validate as icon_validate
from insight_plugin.constants import VALIDATE_DESCRIPTION


class ValidateController(CommonFeature):
    """
    Controls the subcommand for validate
    Allows the user to run validation checks against the plugin
    """

    HELP_MSG = VALIDATE_DESCRIPTION

    def __init__(self, spec_path: str):
        super().__init__()
        self.spec_path = spec_path

    @classmethod
    def new_from_cli(cls, **kwargs):
        super().new_from_cli(**{"spec_path": kwargs.get("spec_path")})
        return cls(
            kwargs.get("spec_path"),
        )

    def validate(self):
        return icon_validate(self.spec_path, run_all=True)
