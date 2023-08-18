from argparse import ArgumentParser

from wesync.services.config.configManager import ConfigManager
from wesync.services.initializationService import InitializationService
from wesync.commands.operationManager import Operation


class ConfigPurgeOperation(Operation):
    operationName = 'purge'

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config

    def run(self):
        initializationService = InitializationService(self.config)
        initializationService.purge()

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--full", action="store_true")
        return argumentParser

