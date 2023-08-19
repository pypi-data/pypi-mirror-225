from wesync.services.config.localConfig import LocalConfigData
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from argparse import ArgumentParser
from wesync.services.config.resolvers.projectConfigResolver import ProjectConfigResolver


class ConfigSync:

    def __init__(self, localConfigData: LocalConfigData, arguments: ArgumentParser):
        self.localConfigData = localConfigData
        self.defaultResolver = ProjectConfigResolver()
        self.arguments = arguments

    def createDeployment(self, project: ProjectConfigData, **kwargs) -> DeploymentConfigData:
        project.ensureKeysAreSet(['name'])
        projectName = project.getName()

        newDeployment = DeploymentConfigData(project)
        for key, value in kwargs.items():
            newDeployment.set(key, value)

        newDeployment.ensureKeysAreSet(['name'])
        deploymentName = newDeployment.getName()

        if existingDeployment := self.localConfigData.getDeploymentByName(projectName, deploymentName):
            return existingDeployment
        else:
            return newDeployment

    def createProject(self, **kwargs) -> ProjectConfigData:
        newProject = ProjectConfigData()
        for key, value in kwargs.items():
            newProject.set(key, value)

        newProject.ensureKeysAreSet(['name'])
        projectName = newProject.getName()

        if existingProject := self.localConfigData.getProjectByName(projectName):
            return existingProject
        else:
            return newProject

    def registerProject(self, project: ProjectConfigData):
        project.ensureKeysAreSet()
        projectName = project.get('name')

        if projectName:
            self.localConfigData.registerProjectName(projectName, project)
        else:
            raise ValueError("Failed to register new project")

    def registerDeployment(self, deployment: DeploymentConfigData):
        deployment.ensureKeysAreSet(['name', 'path', 'host'])
        deploymentName = deployment.getName()

        if deploymentName:
            self.localConfigData.registerDeploymentName(deploymentName, deployment)
        else:
            raise ValueError("Failed to register new deployment")