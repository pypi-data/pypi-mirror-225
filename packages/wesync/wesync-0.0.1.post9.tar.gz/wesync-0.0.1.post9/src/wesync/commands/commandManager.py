from wesync.services.config.configManager import ConfigManager
from argparse import ArgumentParser


class Command:

    requiresConfig = True
    availableOperations = []

    def __init__(self, config: ConfigManager):
        self.config = config

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        return argumentParser

    @classmethod
    def getSupportedCommandOperationArguments(cls) -> list:
        return []


class CommandWithOperations(Command):

    @classmethod
    def getOperations(cls) -> list:
        if not cls.availableOperations:
            raise NotImplementedError("Operations are missing from CommandWithOperations")
        return cls.availableOperations

    @classmethod
    def getOperationByName(cls, operationName: str) -> callable:
        for operationClass in cls.getOperations():
            if hasattr(operationClass, 'operationName'):
                if getattr(operationClass, 'operationName') == operationName:
                    return operationClass
        return None

    @classmethod
    def getSupportedCommandOperationArguments(cls) -> list:
        operationNames = []
        for operationClass in cls.getOperations():
            if operationName := getattr(operationClass, 'operationName'):
                operationNames.append(operationName)
        return operationNames

    def run(self, operation=None, **kwargs):
        operationName = operation or self.config.get('operation')
        operationClass = self.getOperationByName(operationName)
        if not operationClass:
            raise ValueError("Operation {} was not found".format(operationName))

        operation = operationClass(config=self.config, **kwargs)
        return operation.run()