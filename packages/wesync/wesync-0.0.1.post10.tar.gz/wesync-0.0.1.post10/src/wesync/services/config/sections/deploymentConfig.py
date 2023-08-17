from wesync.services.config.sections.configData import SectionConfigData
from wesync.services.config.resolvers.deploymentConfigResolver import DeploymentConfigResolver
from wesync.services.config.sections.projectConfig import ProjectConfigData


class DeploymentConfigData(SectionConfigData):

    mandatoryKeys = ['name', 'path', 'host', 'port', 'username']
    optionalKeys = ['hostname']

    def __init__(self, project: ProjectConfigData):
        super(DeploymentConfigData, self).__init__()
        self.project = project

    def isLocal(self) -> bool:
        defaultResolve = DeploymentConfigResolver()
        if self.get('host') == defaultResolve.resolveHost():
            return True
        return False

    def getName(self):
        return self.get('name')

    def getPath(self):
        return self.get('path')

    def isProtected(self):
        protectedConfig = self.get('protected')
        if protectedConfig is None:
            return self.getName() in ['stg', 'staging', 'prod', 'production']
        return protectedConfig

    def getProjectName(self):
        return self.project.getName()

    def getProject(self) -> ProjectConfigData:
        return self.project

    def ensureKeysAreSet(self, keys: list = None, projectData: dict = None):
        if not projectData:
            projectData = self.project.getData()
        if keys is None:
            keys = self.mandatoryKeys

        for key in keys:
            if not self.has(key):
                defaultResolve = DeploymentConfigResolver(**self.getData())
                defaultResolve.withProjectData(projectData)
                self.setKeyFromInput(key, defaultResolve.resolveKey(key), "deployment")

    def __str__(self):
        str = "Deployment {} {}\n".format(
            self.getProjectName(),
            self.getName()
        )
        str += '\n'.join(["\t{}: {}".format(key, value) for key, value in self.getData().items()])
        return str