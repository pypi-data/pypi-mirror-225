import logging
import subprocess
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager


class RemoteCommandExecutor:

    sshBinary = "ssh"

    def __init__(self, config: ConfigManager, deployment: DeploymentConfigData):
        self.config = config
        self.deployment = deployment

    def _getSSHCommands(self) -> list:
        sshArgs = [
            self.sshBinary, "-A",
            "-p", str(self.deployment.get('port')),
            "-l", self.deployment.get('username'),
            "-o", "StrictHostKeyChecking=no",
            self.deployment.get('host')
        ]

        return sshArgs

    def getArgs(self, args):
        baseArgs = self._getSSHCommands()
        return baseArgs + args

    def execute(self, args, **kwargs):
        baseArgs = self._getSSHCommands()

        if kwargs.get('shell') is True:
            kwargs['shell'] = False
            baseArgs += ["bash", "-c"]

            shellCommand = '"'
            if 'cwd' in kwargs:
                cwd = kwargs.pop('cwd')
                shellCommand += 'cd {}; '.format(cwd)

            shellCommand += ' '.join(args).replace('"', '\\"')
            shellCommand += '"'

            args = [shellCommand]

        args = baseArgs + args

        if self.config.get('dry-run'):
            logging.debug("Dry run: %s %s", args, kwargs)
            return

        logging.debug(' '.join(args))

        ignoreRC = kwargs.pop("ignoreRC", False)

        processResult = subprocess.run(args, capture_output=True)

        if stdout := processResult.stdout.decode():
            logging.log(5, stdout)
        if stderr := processResult.stderr.decode():
            logging.log(5, stderr)

        if ignoreRC is not True:
            if processResult.returncode != 0:
                logging.error("Failed to complete cmd operation %s. RC %d", args, processResult.returncode)
                raise RuntimeError("Failed to complete command {}".format(args))

        return processResult

