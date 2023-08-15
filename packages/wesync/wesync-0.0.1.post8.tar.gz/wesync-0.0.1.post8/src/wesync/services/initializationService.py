import logging
import os
from wesync.services.execute.localCommandExecutor import LocalCommandExecutor
from wesync.services.config.configManager import ConfigManager
from wesync.services.config.remoteConfig import RemoteConfigService


class InitializationService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.executor = LocalCommandExecutor(config)
        self.remoteDataConfig = RemoteConfigService(config)

    def purge(self):
        if self.config.get('full') is True:
            purgeDir = self.config.getWorkDir()
        else:
            purgeDir = self.config.getConfigDir()

        if os.path.exists(purgeDir):
            logging.info("Purging directory {}".format(purgeDir))
            self.executor.execute(["rm", "-r", "-f", purgeDir])

    def initAll(self):
        self.createWorkingDirectory()
        self.createConfigDirectory()
        self.createStashDirectory()
        self.remoteDataConfig.cloneConfigRepository()

    def createWorkingDirectory(self):
        workdir = self.config.getWorkDir()
        if not os.path.exists(workdir):
            logging.info("Creating directory {}".format(workdir))
            self.executor.execute(["mkdir", "-p", "-v", workdir])

    def createConfigDirectory(self):
        configdir = self.config.getConfigDir()
        if not os.path.exists(configdir):
            logging.info("Creating directory {}".format(configdir))
            self.executor.execute(["mkdir", "-p", "-v", configdir])

    def createStashDirectory(self):
        stashdir = self.config.getStashDir()
        if not os.path.exists(stashdir):
            logging.info("Creating directory {}".format(stashdir))
            self.executor.execute(["mkdir", "-p", "-v", stashdir])
