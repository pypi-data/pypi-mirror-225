from .deploymentCommand import DeploymentCommand
from .deploymentList import DeploymentListOperation
from .deploymentAdd import DeploymentAddOperation
from .deploymentDelete import DeploymentDeleteOperation

DeploymentCommand.availableOperations = [
    DeploymentListOperation
]

