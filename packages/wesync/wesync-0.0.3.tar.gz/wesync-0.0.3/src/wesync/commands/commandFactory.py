from wesync.commands.snapshot.snapshotCommand import SnapshotCommand
from wesync.commands.deployment.deploymentCommand import DeploymentCommand
from wesync.commands.config.configCommand import ConfigCommand
from wesync.commands.sync.syncCommand import SyncCommand
from wesync.commands.version.versionCommand import VersionCommand

from wesync.commands.commandManager import Command


class CommandFactory:

    commandNameProperty = 'commandName'

    @staticmethod
    def getKnownCommands() -> list:
        return [
            SnapshotCommand,
            DeploymentCommand,
            ConfigCommand,
            SyncCommand,
            VersionCommand
        ]

    @staticmethod
    def getCommandFor(commandName: str) -> callable:
        for knownCommand in CommandFactory.getKnownCommands():  # type: Command
            if hasattr(knownCommand, CommandFactory.commandNameProperty):
                if getattr(knownCommand, CommandFactory.commandNameProperty) == commandName:
                    return knownCommand

    @classmethod
    def getSupportedCommandArguments(cls) -> list:
        commandNames = []
        for commandClass in CommandFactory.getKnownCommands():
            if commandName := getattr(commandClass, cls.commandNameProperty):
                commandNames.append(commandName)
        return commandNames
