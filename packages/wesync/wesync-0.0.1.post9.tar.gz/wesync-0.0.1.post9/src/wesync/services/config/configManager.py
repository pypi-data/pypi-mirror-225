import os
from wesync.services.config.localConfigManager import LocalConfigManager
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configSync import ConfigSync
from wesync.services.helpers.network import getDefaultIP
from wesync.services.interaction.deploymentQuestions import DeploymentQuestions
from wesync.services.interaction.projectQuestions import ProjectQuestions


class ConfigManager:

    def __init__(self, arguments):
        self.arguments = arguments
        self.localConfigData = None
        self.configSync = None
        self.localConfigManager = LocalConfigManager(
            self.getWorkDir() + "/config"
        )

    def initConfig(self):
        self.localConfigData = self.localConfigManager.loadConfig()
        self.configSync = ConfigSync(
            self.localConfigData,
            self.arguments
        )

    def getCurrentProject(self) -> ProjectConfigData:
        currentProject = None
        if projectName := self.get('project'):
            currentProject = self.localConfigData.getProjectByName(projectName)

        if currentProject is None:
            currentWorkingDirectory = os.getcwd()
            host = getDefaultIP()
            deployment = self.localConfigData.getDeploymentByHostAndPath(host, currentWorkingDirectory)
            if deployment:
                currentProject = deployment.getProject()

        while currentProject is None:
            projectName = ProjectQuestions(self).chooseProject()
            currentProject = self.localConfigData.getProjectByName(projectName)

        self.arguments.project = currentProject.getName()
        return currentProject

    def getDeployment(self, project: ProjectConfigData = None, configKey: str = 'deployment') -> DeploymentConfigData:
        currentDeployment = None
        deploymentName = self.get(configKey)

        if deploymentName is None:
            currentWorkingDirectory = os.getcwd()
            host = getDefaultIP()
            currentDeployment = self.localConfigData.getDeploymentByHostAndPath(host, currentWorkingDirectory)

        if project is None:
            project = self.getCurrentProject()
        else:
            if currentDeployment.getProject() == project:
                return currentDeployment

        if currentDeployment is None and deploymentName:
            currentDeployment = self.localConfigData.getDeploymentByName(project.getName(), deploymentName)

        while currentDeployment is None:
            deploymentName = DeploymentQuestions(self).chooseDeployment(project.getName())
            currentDeployment = self.localConfigData.getDeploymentByName(project.getName(), deploymentName)

        self.set(configKey, currentDeployment.getName())
        return currentDeployment

    def getStashDir(self):
        return self.getWorkDir() + "/stash"

    def getConfigRepository(self):
        return self.get('config-repository', 'ssh://git@git.welink.ro:2424/project/internal/wesync/configuration.git')

    def getWorkDir(self) -> str:
        return os.path.expanduser(self.get('workdir', '~/wesync'))

    def getConfigDir(self) -> str:
        return self.getWorkDir() + "/config"

    def dryRun(self) -> bool:
        return self.get('dry-run', False)

    def getProjectKey(self, projectName: str, key: str, default: str = None):
        projectData = self.localConfigData.getProjectByName(projectName)
        if not projectData:
            return default
        return projectData.get(key, default)

    def getCommand(self):
        return self.get('command')

    def get(self, key: str, default=None):
        value = vars(self.arguments).get(key, None)
        if value is None:
            value = vars(self.arguments).get(key.replace('-', '_'), None)
        if value is None and self.localConfigData:
            return self.localConfigData.getDefaults(key, default)
        if value is None:
            return default
        return value

    def set(self, key, value):
        setattr(self.arguments, key, value)
