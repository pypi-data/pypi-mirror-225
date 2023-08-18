from wesync.services.operations.drupalOperations import DrupalOperationsService
from wesync.services.operations.wordpressOperations import WordpressOperationsService
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from collections import defaultdict


class ProjectManagerFactory:
    managers = defaultdict(lambda: {})

    @classmethod
    def getProjectManagerFor(cls, deployment: DeploymentConfigData, config: ConfigManager, rebuild: bool = False):
        project = deployment.getProject()
        projectType = project.getType()
        projectName = project.getName()
        deploymentName = deployment.getName()

        if manager := cls.managers.get(projectName, {}).get(deploymentName) and rebuild is False:
            return manager

        if projectType == 'drupal':
            manager = DrupalOperationsService(deployment, config)
        elif projectType == 'wordpress':
            manager = WordpressOperationsService(deployment, config)
        else:
            manager = None

        cls.managers[projectName][projectType] = manager

        if manager:
            return manager
        else:
            raise ModuleNotFoundError("Could not find manager to handle {} project type".format(projectType))
