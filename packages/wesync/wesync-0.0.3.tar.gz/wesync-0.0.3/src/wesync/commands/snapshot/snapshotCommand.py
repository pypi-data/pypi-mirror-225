from wesync.commands.commandManager import CommandWithOperations
from wesync.services.snapshot import SnapshotManager
from argparse import ArgumentParser


class SnapshotCommand(CommandWithOperations):

    commandName = 'snapshot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deployment = None
        self.project = None
        self.projectManager = None
        self.snapshotManager = SnapshotManager(self.config)

    def run(self, **kwargs):
        super(SnapshotCommand, self).run(**kwargs)

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--type", type=str, choices=['drupal', 'wordpress'], required=False)
        argumentParser.add_argument("--stash", help="Path of the stash", required=False)
        argumentParser.add_argument("--project", help="Project to lookup in config")
        argumentParser.add_argument("--deployment", help="Deployment to lookup in config")

        return argumentParser

