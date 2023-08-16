from insight_plugin.features.common.common_feature import CommonFeature
from insight_plugin.constants import VIEW_DESCRIPTION
from insight_plugin.features.common.docker_util import DockerUtil


class ViewController(CommonFeature):

    HELP_MSG = VIEW_DESCRIPTION

    def __init__(self, verbose: bool, target_dir: str):
        super().__init__(verbose=verbose, target_dir=target_dir)
        self._verbose = verbose
        self._target_dir = target_dir

    @classmethod
    def new_from_cli(cls, **kwargs):
        super().new_from_cli(
            **{
                "verbose": kwargs.get("verbose"),
                "target_dir": kwargs.get("target_dir"),
            }
        )
        return cls(
            kwargs.get("verbose"),
            kwargs.get("target_dir"),
        )

    def run(self) -> None:
        docker_util = DockerUtil(
            verbose=self._verbose, target_dir=self._target_dir, view=True
        )

        docker_util.run_docker_command()
