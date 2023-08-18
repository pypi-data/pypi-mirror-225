import logging
from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.operations.projectOperations import ProjectOperationsService
from .processor import Processor


class RunShellCmd(ProjectOperationsService, Processor):

    names = ["run-shell-cmd"]
    name = "shell-cmd"

    def __init__(self, processorConfig: ProcessorConfigData, *args, **kwargs):
        self.processorConfig = processorConfig
        super().__init__(*args, **kwargs)
        Processor.__init__(self)

    def execute(self, command: str = None, ignoreFailed: bool = None):
        super(RunShellCmd, self).execute()

        if command is None:
            command = self.processorConfig.get('command')
        if ignoreFailed is None:
            ignoreFailed = self.processorConfig.get('ignoreFailed', False)

        if not command:
            logging.warning("Skipping shell-cmd because command is empty")
            return

        logging.info("Running {}: {}".format(self.name, command))
        commandResult = self.runCommand([command], shell=True, ignoreRC=ignoreFailed)

        if commandResult.returncode != 0:
            logging.info(commandResult.stdout.decode())
            logging.error(commandResult.stderr.decode())
