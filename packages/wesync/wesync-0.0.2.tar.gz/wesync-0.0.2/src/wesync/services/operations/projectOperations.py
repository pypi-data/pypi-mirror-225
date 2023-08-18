import logging
import uuid
import os.path
import re
from wesync.services.snapshot import Snapshot
from .commonOperations import CommonOperationsService


class ProjectOperationsService(CommonOperationsService):

    defaultFilePathArtifacts = [{
        "name": "project.tar.gz",
        "path": "."
    }]

    def __init__(self, *args, **kwargs):
        super(ProjectOperationsService, self).__init__(*args, **kwargs)
        self.artifactsConfig = self.deployment.getProject().getArtifacts()
        self.project = self.deployment.getProject()

    def getFilePathArtifacts(self) -> list:
        filePathArtifacts = []
        for artifactConfig in self.artifactsConfig:
            if artifactConfig.get('type') == 'filepath':
                filePathArtifacts.append(artifactConfig)

        if not filePathArtifacts:
            return self.defaultFilePathArtifacts
        return filePathArtifacts

    def exportFileArtifacts(self, snapshot: Snapshot):
        for artifactConfig in self.getFilePathArtifacts():
            path = artifactConfig.get('path')
            name = artifactConfig.get('name')
            if not name or not path:
                raise ValueError("Path or name missing from artifact config")
            snapshotPath = snapshot.getPath(name)
            self.exportFiles(snapshotPath, path)

    def importFileArtifacts(self, snapshot: Snapshot):
        for artifactConfig in self.getFilePathArtifacts():
            path = artifactConfig.get('path')
            name = artifactConfig.get('name')
            if not name or not path:
                raise ValueError("Path or name missing from artifact config")
            snapshotPath = snapshot.getPath(name)
            self.importFiles(snapshotPath, path)

    def createTempSnapshot(self) -> Snapshot:
        projectName = self.deployment.getProject().getName()
        tmpDirName = '/var/tmp/westash/' + projectName + "_" + uuid.uuid4().hex[:8]
        self.deletePath(tmpDirName, recursive=True, force=True)
        self.createPath(tmpDirName)
        remoteSnapshot = Snapshot(tmpDirName)
        return remoteSnapshot

    def exportFiles(self, archiveExportFile, path):
        path = os.path.normpath(re.sub(r'^(/+)', '', path))

        rootDir = self.deployment.getPath()
        pathDirectories = path.split("/")

        if len(pathDirectories) > 1:
            path = pathDirectories[-1]
            rootDir = rootDir + "/" + '/'.join(pathDirectories[:-1])

        self.archiveFiles(rootPath=rootDir, files=[path], outputArchiveFile=archiveExportFile)

    def importFiles(self, archiveImportFile, path):
        rootDir = self.deployment.getPath()

        path = os.path.normpath(re.sub(r'^(/+)', '', path))
        pathDirectories = path.split("/")

        if len(pathDirectories) > 1:
            path = pathDirectories[-1]
            rootDir = rootDir + "/" + '/'.join(pathDirectories[:-1])

        self.unarchiveFiles(inputArchiveFile=archiveImportFile, rootPath=rootDir, files=[path], delete=True)

    def runCommand(self, args, **kwargs):
        return super(ProjectOperationsService, self).runCommand(args, cwd=self.deployment.getPath(), **kwargs)