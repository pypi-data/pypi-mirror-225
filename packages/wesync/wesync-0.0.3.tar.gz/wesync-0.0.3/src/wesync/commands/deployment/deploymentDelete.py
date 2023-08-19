import logging

from wesync.services.config.configManager import ConfigManager
from wesync.services.config.localConfig import ProjectConfigData
from wesync.commands.operationManager import Operation
from wesync.services.interaction.userInteraction import UserInteraction


class DeploymentDeleteOperation(Operation):

    operationName = 'delete'

    def __init__(self, project: ProjectConfigData, config: ConfigManager):
        super().__init__()
        self.project = project
        self.config = config
        self.project.ensureKeysAreSet(['name'])

    def run(self):
        self.project.ensureKeysAreSet(['name'])
        projectName = self.project.getName()

        deployments = self.config.localConfigData.getDeploymentsForProject(projectName)
        if not deployments:
            logging.info("Project {} has not deployments".format(projectName))
            return

        deploymentName = self.config.get('deployment-name')
        if not deploymentName:
            deploymentNames = [deployment.getName() for deployment in deployments]
            deploymentNamesString = "(" + ', '.join(deploymentNames) + ")"
            defaultDeployment = None

            if len(deploymentNames) == 1:
                defaultDeployment = deploymentNames[0]

            deploymentName = UserInteraction().askForAnswer(
                "Deployment name to delete {}".format(deploymentNamesString),
                defaultDeployment
            )

        deployment = self.config.localConfigData.getDeploymentByName(projectName, deploymentName)
        if deployment is None:
            logging.error("Cannot find deployment config {} for project {}".format(deploymentName, projectName))
            return

        logging.warning("Will delete the following deployment")
        logging.info(str(deployment))

        if UserInteraction().confirm() is True:
            logging.warning("Deleting deployment")
            self.config.localConfigData.deleteDeployment(deployment.getProjectName(), deployment.getName())
