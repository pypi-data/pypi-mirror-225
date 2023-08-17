import logging

from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.config.remoteConfig import RemoteConfigService
from wesync.services.initializationService import InitializationService
from wesync.services.interaction.userInteraction import UserInteraction


class ConfigUpdateOperation(Operation):
    operationName = 'update'

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config

    def run(self):
        remoteConfigService = RemoteConfigService(self.config)
        if not remoteConfigService.hasConfigDirectory():
            if UserInteraction().confirm("Configuration repository is missing. Clone now ?", default=True) is True:
                initializationService = InitializationService(self.config)
                initializationService.createConfigDirectory()
                remoteConfigService.cloneConfigRepository()

        remoteConfigService.fetchConfigRepository(force=True)
        hasChanges = remoteConfigService.hasChangesInConfigRepository()
        if hasChanges is True:
            remoteConfigService.pullConfigRepository()
        elif hasChanges is False:
            logging.info("No changes in remote repository")
