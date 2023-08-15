from wesync.services.config.configManager import ConfigManager

from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.snapshot import SnapshotManager
from wesync.services.execute.RsyncFileTransferService import RsyncFileTransfer
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData


class DeploymentSyncService:

    def __init__(self, config: ConfigManager):
        self.config = config
        self.rsyncFileTransfer = RsyncFileTransfer(self.config)
        self.snapshotManager = SnapshotManager(self.config)

    def sync(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        project = sourceDeployment.getProject()
        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)
        destinationProjectManager = ProjectManagerFactory.getProjectManagerFor(destinationDeployment, self.config)

        if project.getSyncStrategy() == 'snapshot':
            syncSnapshot = self.snapshotManager.initSnapshot(
                project.getName(),
                self.config.get('label', 'sync')
            )

            if sourceDeployment.isLocal():
                sourceProjectManager.fullExport(syncSnapshot)
            else:
                remoteSnapshot = sourceProjectManager.createTempSnapshot()

                sourceProjectManager.fullExport(remoteSnapshot)

                self.rsyncFileTransfer.copyFromRemote(
                    source=sourceDeployment,
                    sourcePath=remoteSnapshot.getPath() + "/",
                    destinationPath=syncSnapshot.getPath()
                )

                sourceProjectManager.deletePath(remoteSnapshot.getPath(), recursive=True)

            if destinationDeployment.isLocal():
                destinationProjectManager.fullImport(syncSnapshot)
            else:
                remoteSnapshot = destinationProjectManager.createTempSnapshot()

                self.rsyncFileTransfer.copyToRemote(
                    sourcePath=syncSnapshot.getPath() + "/",
                    destination=destinationDeployment,
                    destinationPath=remoteSnapshot.getPath()
                )

                destinationProjectManager.fullImport(remoteSnapshot)

                destinationProjectManager.deletePath(remoteSnapshot.getPath(), recursive=True)

        else:
            raise ValueError("Project has unsupported sync strategy: {}".format(project.getSyncStrategy()))
