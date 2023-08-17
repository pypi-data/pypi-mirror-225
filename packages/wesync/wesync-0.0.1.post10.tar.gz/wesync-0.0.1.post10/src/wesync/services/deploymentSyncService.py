import logging

from wesync.services.config.configManager import ConfigManager

from wesync.services.projectManagerFactory import ProjectManagerFactory
from wesync.services.snapshot import SnapshotManager
from wesync.services.execute.RsyncFileTransferService import RsyncFileTransfer
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.execute.SCPFileTransferService import SCPFileTransfer
from wesync.services.execute.localCommandExecutor import LocalCommandExecutor


class DeploymentSyncService:

    def __init__(self, config: ConfigManager):
        self.config = config
        self.rsyncFileTransfer = RsyncFileTransfer(self.config)
        self.scpFileTransfer = SCPFileTransfer(self.config)
        self.snapshotManager = SnapshotManager(self.config)

    def sync(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        project = sourceDeployment.getProject()
        syncStrategy = self.config.get('sync-strategy', project.getSyncStrategy())

        if syncStrategy == 'snapshot':
            self.syncWithRsyncSnapshot(sourceDeployment, destinationDeployment)
        elif syncStrategy == 'scpSnapshot':
            self.syncWithScpSnapshot(sourceDeployment, destinationDeployment)
        elif syncStrategy == 'rsync':
            self.streamFilesWithRsync(sourceDeployment, destinationDeployment)
            self.streamDatabase(sourceDeployment, destinationDeployment)
        elif syncStrategy == 'scp':
            self.streamFilesWithScp(sourceDeployment, destinationDeployment)
            self.streamDatabase(sourceDeployment, destinationDeployment)
        else:
            raise ValueError("Project has unsupported sync strategy: {}".format(project.getSyncStrategy()))

    def syncWithScpSnapshot(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        if sourceDeployment.isLocal() and destinationDeployment.isLocal():
            raise ValueError("In scp snapshot strategy, at least one deployment must be remote")

        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)
        destinationProjectManager = ProjectManagerFactory.getProjectManagerFor(destinationDeployment, self.config)

        sourceSnapshot = sourceProjectManager.createTempSnapshot()
        destinationSnapshot = destinationProjectManager.createTempSnapshot()

        sourceProjectManager.fullExport(sourceSnapshot)

        if not sourceDeployment.isLocal() and destinationDeployment.isLocal():
            self.scpFileTransfer.copyFromRemote(sourceDeployment, sourceSnapshot.getPath(), destinationSnapshot.getPath())
        elif sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            self.scpFileTransfer.copyToRemote(sourceSnapshot.getPath(), destinationDeployment, destinationSnapshot.getPath())
        elif not sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            self.scpFileTransfer.copyBetweenRemotes(sourceDeployment, sourceSnapshot.getPath(),
                                                    destinationDeployment, destinationSnapshot.getPath())

        destinationProjectManager.fullImport(destinationSnapshot)

        sourceProjectManager.deletePath(sourceSnapshot.getPath(), recursive=True)
        destinationProjectManager.deletePath(destinationSnapshot.getPath(), recursive=True)

    def streamDatabase(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)
        destinationProjectManager = ProjectManagerFactory.getProjectManagerFor(destinationDeployment, self.config)

        exportArguments = sourceProjectManager.exportDatabaseToStdout(returnExecutorArgs=True)
        importArguments = destinationProjectManager.importDatabaseFromStdin(returnExecutorArgs=True)

        logging.info("Streaming database from {} to {}".format(sourceDeployment.getName(), destinationDeployment.getName()))
        localCommandExecutor = LocalCommandExecutor(self.config)
        localCommandExecutor.pipe(exportArguments, importArguments)

    def streamFilesWithRsync(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        if not sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            raise ValueError("In rsync strategy, at least one deployment must be local")

        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)

        logging.info("Streaming files from {} to {}".format(sourceDeployment.getName(), destinationDeployment.getName()))
        if not sourceDeployment.isLocal() and destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.rsyncFileTransfer.copyFromRemote(
                    source=sourceDeployment,
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )

        elif sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.rsyncFileTransfer.copyToRemote(
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destination=destinationDeployment,
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )
        elif sourceDeployment.isLocal() and destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.rsyncFileTransfer.copy(
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )

    def streamFilesWithScp(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        if sourceDeployment.isLocal() and destinationDeployment.isLocal():
            raise ValueError("In scp strategy, at least one deployment must be remote")

        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)

        logging.info("Streaming files from {} to {}".format(sourceDeployment.getName(), destinationDeployment.getName()))
        if not sourceDeployment.isLocal() and destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.scpFileTransfer.copyFromRemote(
                    source=sourceDeployment,
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )

        elif sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.scpFileTransfer.copyToRemote(
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destination=destinationDeployment,
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )
        elif not sourceDeployment.isLocal() and not destinationDeployment.isLocal():
            for fileArtifact in sourceProjectManager.getFilePathArtifacts():
                fileArtifactPath = fileArtifact.get('path')
                self.scpFileTransfer.copyBetweenRemotes(
                    source=sourceDeployment,
                    sourcePath='/'.join([sourceDeployment.getPath(), fileArtifactPath, '']),
                    destination=destinationDeployment,
                    destinationPath='/'.join([destinationDeployment.getPath(), fileArtifactPath])
                )

    def syncWithRsyncSnapshot(self, sourceDeployment: DeploymentConfigData, destinationDeployment: DeploymentConfigData):
        project = sourceDeployment.getProject()
        sourceProjectManager = ProjectManagerFactory.getProjectManagerFor(sourceDeployment, self.config)
        destinationProjectManager = ProjectManagerFactory.getProjectManagerFor(destinationDeployment, self.config)

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
