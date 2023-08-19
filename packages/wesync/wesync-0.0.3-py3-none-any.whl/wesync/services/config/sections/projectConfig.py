from wesync.services.interaction.userInteraction import UserInteraction
from wesync.services.config.resolvers.projectConfigResolver import ProjectConfigResolver
from wesync.services.config.sections.configData import SectionConfigData
from .hasProcessors import HasProcessors


class ProjectConfigData(HasProcessors, SectionConfigData):

    mandatoryKeys = ["name", "type"]
    optionalKeys = ["artifacts", "syncStrategy"]

    def __init__(self):
        super(ProjectConfigData, self).__init__()
        self.interaction = UserInteraction()
        self.deployments = []

    def getName(self) -> str:
        return self.get('name').lower()

    def getType(self):
        return self.get('type')

    def getDeployments(self):
        return self.deployments

    def getPath(self):
        return self.get('path')

    def getArtifacts(self):
        return self.get('artifacts', [])

    def getSyncStrategy(self):
        return self.get('syncStrategy', 'snapshot')

    def ensureKeysAreSet(self, keys: list = None):
        if keys is None:
            keys = self.mandatoryKeys

        for key in keys:
            if not self.has(key):
                defaultResolve = ProjectConfigResolver(**self.getData())
                self.setKeyFromInput(key, defaultResolve.resolveKey(key), "project")

    def attachDeployment(self, deployment):
        self.deployments.append(deployment)
