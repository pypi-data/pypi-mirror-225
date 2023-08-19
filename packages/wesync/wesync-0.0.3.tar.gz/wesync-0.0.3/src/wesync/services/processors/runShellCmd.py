import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from .processor import Processor, ProcessorResult


class RunShellCmd(Processor, ProjectOperationsService):

    names = ["run-shell-cmd"]
    name = "shell-cmd"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, command: str = None, ignoreFailed: bool = None, **kwargs) -> ProcessorResult:
        super(RunShellCmd, self).execute()

        if command is None:
            command = self.processorConfig.get('command')
        if ignoreFailed is None:
            ignoreFailed = self.processorConfig.get('ignoreFailed', False)

        if not command:
            logging.warning("Skipping shell-cmd because command is empty")
            return ProcessorResult()

        logging.info("Running {}: {}".format(self.name, command))
        commandResult = self.runCommand([command], shell=True, ignoreRC=ignoreFailed)

        if commandResult.returncode != 0:
            logging.info(commandResult.stdout.decode())
            logging.error(commandResult.stderr.decode())

        return ProcessorResult(commandResult=commandResult)
