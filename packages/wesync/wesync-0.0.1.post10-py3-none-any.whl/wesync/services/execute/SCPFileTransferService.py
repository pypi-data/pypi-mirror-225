from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from .localCommandExecutor import LocalCommandExecutor


class SCPFileTransfer:

    scpBinary = "scp"

    def __init__(self, config: ConfigManager):
        self.config = config
        self.localCommandExecutor = LocalCommandExecutor(self.config)

    def copyFromRemote(self, source, sourcePath: str, destinationPath: str):
        if isinstance(source, DeploymentConfigData):
            args = [
                self.scpBinary,
                "-P", str(source.get('port')),
                "-p", "-r", "-B",
                "{}@{}:{}".format(
                    source.get('username'),
                    source.get('host'),
                    sourcePath
                ),
                destinationPath
            ]
        else:
            raise ValueError("Source is not supported: {}".format(source))

        return self.localCommandExecutor.execute(args)

    def copyToRemote(self, sourcePath: str, destination, destinationPath: str):
        if isinstance(destination, DeploymentConfigData):
            args = [
                self.scpBinary,
                "-P", str(destination.get('port')),
                "-p", "-r", "-B",
                sourcePath,
                "{}@{}:{}".format(
                    destination.get('username'),
                    destination.get('host'),
                    destinationPath
                )
            ]
        else:
            raise ValueError("Destination is not supported: {}".format(destination))

        return self.localCommandExecutor.execute(args)

    def copyBetweenRemotes(self, source, sourcePath: str, destination, destinationPath: str):
        args = [self.scpBinary, "-p", "-r", "-B", "-3"]

        if isinstance(source, DeploymentConfigData):
            args += [
                "{}@{}:{}".format(
                    source.get('username'),
                    source.get('host'),
                    sourcePath
                )
            ]
        else:
            raise ValueError("Source is not supported: {}".format(source))

        if isinstance(destination, DeploymentConfigData):
            args += [
                "{}@{}:{}".format(
                    destination.get('username'),
                    destination.get('host'),
                    destinationPath
                )
            ]
        else:
            raise ValueError("Destination is not supported: {}".format(destination))

        return self.localCommandExecutor.execute(args)
