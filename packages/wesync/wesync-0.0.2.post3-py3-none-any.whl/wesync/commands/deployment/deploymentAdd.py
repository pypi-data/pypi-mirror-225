from wesync.services.config.configManager import ConfigManager
from wesync.services.config.localConfig import ProjectConfigData
from wesync.commands.operationManager import Operation
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData


class DeploymentAddOperation(Operation):

    operationName = 'add'

    def __init__(self, project: ProjectConfigData, config: ConfigManager):
        super().__init__()
        self.project = project
        self.config = config
        self.project.ensureKeysAreSet(['name'])

    def run(self):
        self.project.ensureKeysAreSet(['name', 'path', 'type'])

        newDeployment = DeploymentConfigData(self.project)

        newDeployment.ensureKeysAreSet(
            ["name", "path", "host", "port", "username"]
        )

        self.config.localConfigData.registerDeploymentName(
            newDeployment.getName(),
            newDeployment
        )



