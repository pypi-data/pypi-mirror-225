import logging
from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData


class ProcessorResult():
    def __init__(self, newArguments: dict = None, commandResult=None):
        self.newArguments = newArguments or {}
        self.commandResult = commandResult


class Processor():

    name = "processor"
    projectTypes = ['*']

    def __init__(self, processorConfig: ProcessorConfigData, *args, **kwargs):
        self.processorConfig = processorConfig
        self.userInteraction = UserInteraction()
        self.deployment = kwargs.get('deployment')      # type: DeploymentConfigData
        super().__init__(*args, **kwargs)

    def askForArgument(self, argument: str, **kwargs):
        return self.userInteraction.askForAnswer(self.name + " value for '" + argument + "'", **kwargs)

    def resolveSearchAndReplace(self, **kwargs):
        searchAndReplaceOld = kwargs.get('searchAndReplaceOld')
        searchAndReplaceNew = kwargs.get('searchAndReplaceNew')

        if searchAndReplaceOld is None:
            searchAndReplaceOld = self.processorConfig.get('old')
            if searchAndReplaceOld is None:
                searchAndReplaceOld = self.askForArgument('old', allowEmpty=True)

        if not searchAndReplaceOld:
            logging.warning("Skipping {} because one term is empty".format(self.name))
            return

        if searchAndReplaceNew is None:
            searchAndReplaceNew = self.deployment.get('hostname')
            if not searchAndReplaceNew:
                self.askForArgument('new', allowEmpty=True)

        if not searchAndReplaceNew:
            logging.warning("Skipping {} because one term is empty".format(self.name))
            return

        if searchAndReplaceOld == searchAndReplaceNew:
            logging.warning("Skipping {} because terms are the same".format(self.name))
            return

        return searchAndReplaceOld, searchAndReplaceNew

    def execute(self, *args, **kwargs) -> ProcessorResult:
        logging.log(1, "Running " + self.name)


