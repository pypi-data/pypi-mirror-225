import logging
from argparse import ArgumentParser

from wesync.services.snapshot import SnapshotManager
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation


class SnapshotDeleteOperation(Operation):

    operationName = 'delete'

    def __init__(self, config: ConfigManager, **kwargs):
        super().__init__()
        self.config = config

        self.project = self.config.getCurrentProject()

        self.snapshotManager = SnapshotManager(self.config)

    def run(self):
        if path := self.config.get('path'):
            if self.project.getName() not in path:
                raise ValueError("Snapshot path is not for the project")
            self.snapshotManager.deleteByPath(path)
        elif label := self.config.get('label'):
            self.snapshotManager.deleteByLabel(self.project.getName(), label)
        else:
            logging.error("Please specify label or path when deleting")

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--label", help="Label of the snapshot")
        argumentParser.add_argument("--path", help="Path of the snapshot")
        return argumentParser