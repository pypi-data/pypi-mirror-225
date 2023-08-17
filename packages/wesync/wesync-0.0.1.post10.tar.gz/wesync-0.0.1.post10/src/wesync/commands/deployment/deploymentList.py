import logging
from wesync.services.config.configManager import ConfigManager
from wesync.services.config.localConfig import ProjectConfigData
from wesync.commands.operationManager import Operation


class DeploymentListOperation(Operation):

    operationName = 'list'

    def __init__(self, project: ProjectConfigData, config: ConfigManager):
        super().__init__()
        self.project = project
        self.config = config
        self.project.ensureKeysAreSet(['name'])

    def run(self):
        projectName = self.project.getName()
        deployments = self.config.localConfigData.getDeploymentsForProject(projectName)

        logging.info("{} deployments for project {}".format(len(deployments), projectName))
        for deployment in deployments:
            logging.info(str(deployment))