import logging
import os
from collections import defaultdict
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData


class LocalConfigData:
    def __init__(self):
        self.defaults = {}
        self.aliases = defaultdict(lambda: {})
        self.projects = {}
        self.deployments = defaultdict(lambda: {})

    # Manage projects #
    def registerProjectName(self, projectName: str, projectConfigData: ProjectConfigData):
        self.projects[projectName.lower()] = projectConfigData

    def registerProject(self, projectConfigData: ProjectConfigData):
        projectName = projectConfigData.getName()
        logging.log(5, "Loading project {}: {}".format(projectName, projectConfigData))
        self.projects[projectName] = projectConfigData

    def getProjectByName(self, projectName: str):
        return self.projects.get(projectName.lower())

    # Manage deployments #
    def registerDeployment(self, deploymentConfigData: DeploymentConfigData):
        project = deploymentConfigData.getProject()
        deploymentName = deploymentConfigData.getName()
        self.deployments[project.getName()][deploymentName] = deploymentConfigData

    def registerDeploymentName(self, deploymentName: str, deploymentConfigData: DeploymentConfigData):
        projectName = deploymentConfigData.getProjectName()
        self.deployments[projectName][deploymentName] = deploymentConfigData

    def getDeploymentsForProject(self, projectNameLookup: str) -> list:
        for projectName, deploymentDict in self.deployments.items():
            if projectName == projectNameLookup:
                return list(deploymentDict.values())
        return []

    def getDeploymentByName(self, projectName: str, deploymentName: str) -> DeploymentConfigData:
        projectName = projectName.lower()
        deploymentName = deploymentName.lower()
        return self.deployments.get(projectName, {}).get(deploymentName, None)

    def deleteDeployment(self, projectName: str, deploymentName: str):
        projectName = projectName.lower()
        deploymentName = deploymentName.lower()
        del(self.deployments[projectName][deploymentName])

    def getDeploymentByHostAndPath(self, host: str, path: str):
        for projectName, deploymentDict in self.deployments.items():
            for deploy in deploymentDict.values():
                if deploy.get('host') == host and self.isSubpathOf(path, deploy.get('path')):
                    return deploy
        return None

    # Configuration helpers #

    def isClean(self):
        for project in self.projects.values():
            if project.isClean() is False:
                return False
        return True

    def getDefaults(self, key: str, default=None):
        return self.defaults.get(key, default)

    def __getattr__(self, argument, default=None):
        return self.getDefaults(argument, default)

    @staticmethod
    def isSubpathOf(path: str, basePath: str) -> bool:
        pathParts = os.path.normpath(path).split('/')
        for i in reversed(range(0, len(pathParts)+1)):
            testPath = '/'.join(pathParts[:i])
            if testPath and testPath == basePath:
                return True

        return False
