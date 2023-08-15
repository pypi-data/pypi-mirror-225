from wesync.commands.commandManager import Command
from argparse import ArgumentParser
from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.deploymentSyncService import DeploymentSyncService
from wesync.services.processors.processorManager import ProcessorManager


class SyncCommand(Command):

    commandName = 'sync'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deploymentSyncService = DeploymentSyncService(self.config)
        self.userInteraction = UserInteraction()
        self.processorManager = ProcessorManager(self.config)

    def run(self, **kwargs):
        sourceDeployment, destinationDeployment = self._getDeployments()
        if destinationDeployment.isProtected():
            if self.userInteraction.confirm("Target deployment is protected. Continue ?") is False:
                return False

        self.deploymentSyncService.sync(sourceDeployment, destinationDeployment)

        importProcessors = self.processorManager.getImportProcessors(destinationDeployment)
        importProcessors.executeAll(searchAndReplaceOld=sourceDeployment.get('hostname'))

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        argumentParser.add_argument("--project", type=str, required=False)
        argumentParser.add_argument("source", help="Deployment name of the source")
        argumentParser.add_argument("destination", help="Deployment name of the destination")
        return argumentParser

    def _getDeployments(self):
        project = self.config.getCurrentProject()
        projectName = project.getName()

        sourceDeploymentName = self.config.get('source')
        destinationDeploymentName = self.config.get('destination')

        if not sourceDeploymentName or not sourceDeploymentName:
            raise ValueError("Could not find deployment {} for project {}".format(sourceDeploymentName, projectName))

        if sourceDeploymentName == '-' and destinationDeploymentName == '-':
            raise ValueError("At least one deployment must be specified".format(sourceDeploymentName, projectName))

        if sourceDeploymentName == '-':
            sourceDeployment = self.config.getDeployment(project)
        else:
            sourceDeployment = self.config.localConfigData.getDeploymentByName(
                projectName,
                sourceDeploymentName
            )

        if sourceDeployment is None:
            raise ValueError("Could not find deployment {} for project {}".format(sourceDeploymentName, projectName))

        if destinationDeploymentName == '-':
            destinationDeployment = self.config.getDeployment(project)
        else:
            destinationDeployment = self.config.localConfigData.getDeploymentByName(
                projectName,
                destinationDeploymentName
            )

        if destinationDeployment is None:
            raise ValueError("Could not find deployment {} for project {}".format(destinationDeploymentName, projectName))

        return sourceDeployment, destinationDeployment
