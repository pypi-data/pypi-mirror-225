from wesync.commands.commandManager import CommandWithOperations
from wesync.services.snapshot import SnapshotManager
from argparse import ArgumentParser


class DeploymentCommand(CommandWithOperations):

    commandName = 'deployment'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = None
        self.projectManager = None
        self.snapshotManager = SnapshotManager(self.config)

    def run(self, **kwargs):
        self.project = self.config.getCurrentProject()
        super(DeploymentCommand, self).run(project=self.project, **kwargs)

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--deployment-name", help="Name of the deployment", required=False)
        return argumentParser

