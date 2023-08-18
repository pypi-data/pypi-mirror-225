from wesync.services.config.sections.configData import SectionConfigData
from wesync.services.config.sections.projectConfig import ProjectConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData


class ProcessorConfigData(SectionConfigData):

    mandatoryKeys = ['name']
    optionalKeys = '*'

    def __init__(self, trigger: str, project: ProjectConfigData = None, deployment: DeploymentConfigData = None):
        super(ProcessorConfigData, self).__init__()
        self.trigger = trigger

        if not deployment and not project:
            raise ValueError("Processor config section requires deployment or project")

        if deployment:
            self.deployment = deployment
            self.project = deployment.getProject()
        if project:
            self.project = project

    def getProject(self) -> ProjectConfigData:
        return self.project

    def getDeployment(self) -> DeploymentConfigData:
        return self.deployment

    def getTrigger(self):
        return self.trigger

    def getName(self):
        return self.get('name')

    def __str__(self):
        return str(self.data)

