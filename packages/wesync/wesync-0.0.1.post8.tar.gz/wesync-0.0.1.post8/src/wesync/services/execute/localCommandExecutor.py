import logging
import subprocess
from wesync.services.config.configManager import ConfigManager


class LocalCommandExecutor:

    sshBinary = "ssh"

    def __init__(self, config: ConfigManager):
        self.config = config

    def execute(self, args, **kwargs):
        if self.config.get('dry-run'):
            logging.debug("Dry run: %s %s", args, kwargs)
            return
        logging.log(5, args)

        ignoreRC = kwargs.pop("ignoreRC", False)

        processResult = subprocess.run(args, capture_output=True, **kwargs)
        stdout = processResult.stdout.decode()
        stderr = processResult.stderr.decode()
        logging.log(5, stdout)
        logging.log(5, stderr)
        if ignoreRC is not True:
            if processResult.returncode != 0:
                logging.error("Failed to complete cmd operation %s. RC %d", args, processResult.returncode)
                raise RuntimeError("Failed to complete command {}".format(args))

        return processResult
