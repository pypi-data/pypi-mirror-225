import argparse
from wesync.commands.commandFactory import CommandFactory


class ArgumentParser:

    def process(self) -> argparse.ArgumentParser:

        argumentParser = argparse.ArgumentParser(prog="Welink Stash", description="Stash Welink", add_help=False)
        argumentParser.add_argument("command", type=str, choices=CommandFactory.getSupportedCommandArguments())
        argumentParser.add_argument("--dry-run", action='store_true', required=False)
        argumentParser.add_argument("--config", help="Path of the config file", required=False)
        argumentParser.add_argument("--debug", action='store_true', required=False)
        argumentParser.add_argument("--verbose", action='store_true', required=False)
        (preliminaryArguments, _) = argumentParser.parse_known_args()

        commandClass = CommandFactory.getCommandFor(preliminaryArguments.command)

        commandClass.configureArguments(argumentParser)
        operationNames = commandClass.getSupportedCommandOperationArguments()
        if operationNames:
            argumentParser.add_argument("operation", type=str, choices=operationNames)

            (preliminaryArguments, _) = argumentParser.parse_known_args()

            operationClass = commandClass.getOperationByName(preliminaryArguments.operation)
            operationClass.configureArguments(argumentParser)

        return argumentParser
