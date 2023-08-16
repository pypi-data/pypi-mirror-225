from insight_plugin.features.common.common_feature import CommonFeature
from insight_plugin.constants import SERVER_DESCRIPTION
from insight_plugin.features.common.docker_util import DockerUtil


class RunServerController(CommonFeature):
    """
    Controls the subcommand for Run Server
    Allows the user to run the plugin as a webserver
    """

    HELP_MSG = SERVER_DESCRIPTION

    def __init__(
        self,
        verbose: bool,
        target_dir: str,
        volumes: [str],
        ports: [str],
        rebuild: bool,
    ):
        super().__init__(verbose, target_dir)
        self.rebuild = rebuild
        self.volumes = volumes
        self.ports = ports
        self._verbose = verbose

    @classmethod
    def new_from_cli(cls, **kwargs):
        super().new_from_cli(
            **{"verbose": kwargs.get("verbose"), "target_dir": kwargs.get("target_dir")}
        )
        return cls(
            kwargs.get("verbose"),
            kwargs.get("target_dir"),
            kwargs.get("volumes"),
            kwargs.get("ports"),
            kwargs.get("rebuild"),
        )

    def run(self):
        """
        Main run function for Run Server
        :return:
        """
        docker_util = DockerUtil(
            verbose=self.verbose,
            target_dir=self.target_dir,
            volumes=self.volumes,
            ports=self.ports,
            rebuild=self.rebuild,
            server=True,
        )
        docker_util.run_docker_command()
