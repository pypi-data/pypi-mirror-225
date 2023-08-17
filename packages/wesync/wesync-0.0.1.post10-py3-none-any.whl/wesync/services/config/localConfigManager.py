import logging
import os
import yaml
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.sections.processorConfig import ProcessorConfigData
from .localConfig import LocalConfigData


class LocalConfigManager:

    def __init__(self, configDirectory):
        self.configDirectory = configDirectory

    @staticmethod
    def _getfileLocation() -> str:
        configFileLocation = os.path.expanduser("~/wesync/config/")
        if os.path.exists(".wlkconfig.ini"):
            configFileLocation = ".wlkconfig.ini"
        elif os.path.exists(os.path.expanduser("~/.wlkconfig.ini")):
            configFileLocation = os.path.expanduser("~/.wlkconfig.ini")
        return configFileLocation

    def loadConfig(self) -> LocalConfigData:
        localConfigData = LocalConfigData()

        if not self.hasConfig():
            return localConfigData

        projectPath = self.configDirectory + "/projects"
        if not os.path.exists(projectPath):
            return localConfigData

        for project in os.listdir(projectPath):
            if ".yml" in project:
                with open(projectPath + "/" + project, "r") as fd:
                    projectConfigDict = yaml.safe_load(fd)

                project = ProjectConfigData()
                project.loadFromConfig(projectConfigDict)
                localConfigData.registerProject(project)

                for deploymentConfigDict in projectConfigDict.get('deployments', []):
                    deployment = DeploymentConfigData(project)
                    deployment.loadFromConfig(deploymentConfigDict)
                    localConfigData.registerDeployment(deployment)

                for processorTriggerName, processorTriggerData in projectConfigDict.get('processors', {}).items():
                    for processorConfigDict in processorTriggerData:
                        processor = ProcessorConfigData(project, processorTriggerName)
                        processor.loadFromConfig(processorConfigDict)
                        project.addProcessor(processor)

        localConfigData.defaults = {}
        return localConfigData

    def hasConfig(self) -> bool:
        if not os.path.exists(self.configDirectory):
            return False
        if len(os.listdir(self.configDirectory)) == 0:
            return False

        return True
