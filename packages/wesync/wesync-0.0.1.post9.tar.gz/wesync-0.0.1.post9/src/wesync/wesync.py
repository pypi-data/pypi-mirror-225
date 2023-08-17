#!/usr/bin/env python3
import sys
from wesync.common.logging import consoleLogging
import logging
from wesync.services.config.configManager import ConfigManager
from wesync.common.arguments import ArgumentParser
from wesync.commands.commandFactory import CommandFactory
from wesync.services.initializationService import InitializationService
from wesync.services.interaction.userInteraction import UserInteraction


def run():

    args = ArgumentParser().process().parse_args()
    configManager = ConfigManager(args)

    if configManager.get('verbose') is True:
        consoleLogging.setLevel(logging.DEBUG)
    if configManager.get('debug') is True:
        consoleLogging.setLevel(5)
    if configManager.get('debug') is True and configManager.get('verbose') is True:
        consoleLogging.setLevel(1)

    configManager.initConfig()

    commandClass = CommandFactory.getCommandFor(configManager.getCommand())
    if not commandClass:
        logging.error("Could not find command manager for %s", configManager.getCommand())
        sys.exit(300)

    if commandClass.requiresConfig is True:
        if not configManager.localConfigManager.hasConfig():
            if UserInteraction().confirm("Configuration is missing. Create now ?", default=True) is True:
                initializationService = InitializationService(configManager)
                initializationService.initAll()
                configManager.initConfig()
            else:
                sys.exit(0)
        else:
            initializationService = InitializationService(configManager)
            initializationService.remoteDataConfig.fetchConfigRepository()
            if initializationService.remoteDataConfig.isConfigRepositoryOutdated():
                if UserInteraction().confirm("Remote configuration is outdated. Update now ?", default=True):
                    initializationService.remoteDataConfig.pullConfigRepository()
                    configManager.initConfig()

    try:
        commandManager = commandClass(configManager)
    except Exception:
        logging.exception("Failed to initialize command class")
        sys.exit(100)

    try:
        commandManager.run()
    except Exception as e:
        if configManager.get('debug') is True:
            logging.exception(e, exc_info=e)
        else:
            logging.error(e)
        sys.exit(200)


if __name__ == '__main__':
    run()