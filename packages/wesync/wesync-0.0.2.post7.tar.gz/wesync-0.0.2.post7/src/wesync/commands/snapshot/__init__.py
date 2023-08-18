from .snapshotList import SnapshotListOperation
from .snapshotDelete import SnapshotDeleteOperation
from .snapshotPurge import SnapshotPurgeOperation
from .snapshotExport import SnapshotExportOperation
from .snapshotImport import SnapshotImportOperation
from .snapshotCommand import SnapshotCommand

SnapshotCommand.availableOperations = [
    SnapshotListOperation,
    SnapshotDeleteOperation,
    SnapshotPurgeOperation,
    SnapshotImportOperation,
    SnapshotExportOperation
]

