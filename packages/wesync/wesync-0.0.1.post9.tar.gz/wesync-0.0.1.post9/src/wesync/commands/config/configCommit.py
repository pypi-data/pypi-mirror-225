import logging
from datetime import datetime
from wesync.services.config.configManager import ConfigManager
from wesync.commands.operationManager import Operation
from wesync.services.config.remoteConfig import RemoteConfigService
from wesync.services.interaction.userInteraction import UserInteraction


class ConfigCommitOperation(Operation):
    operationName = 'commit'

    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.userInteraction = UserInteraction()

    def run(self):
        remoteConfigService = RemoteConfigService(self.config)
        logging.info("Updating config repository")
        remoteConfigService.fetchConfigRepository(force=True)
        hasChanges = remoteConfigService.hasChangesInConfigRepository()
        if hasChanges is not False:
            logging.error("Repository must be updated without diverging changes")

        timestamp = datetime.now().strftime("%m-%d %H:%M")
        commitMessage = self.userInteraction.askForAnswer("Please enter commit message", default="Updated {}".format(timestamp))

        remoteConfigService.commitConfigRepository(commitMessage=commitMessage)
        remoteConfigService.pushConfigRepository()
