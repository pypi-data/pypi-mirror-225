from .configCommand import ConfigCommand
from .configInit import ConfigInitOperation
from .configPurge import ConfigPurgeOperation
from .configUpdate import ConfigUpdateOperation
from .configCommit import ConfigCommitOperation

ConfigCommand.availableOperations = [
    ConfigInitOperation,
    ConfigPurgeOperation,
    ConfigUpdateOperation,
    ConfigCommitOperation
]

