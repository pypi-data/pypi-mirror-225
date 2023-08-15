import logging
import os
import re
import shutil
from wesync.services.config.configManager import ConfigManager
from datetime import datetime

timestampString = "%Y-%m-%d_%H-%M"


class Snapshot:
    def __init__(self, path):
        self.path = path
        self.projectName = None
        self.timestamp = None
        self.label = None
        self.getPartsFromName()

    @staticmethod
    def nameFromParts(projectName, timestamp=None, label=None):
        timestamp = timestamp if timestamp else datetime.now()
        snapshotName = projectName + "__" + timestamp.strftime(timestampString)
        if label is not None:
            snapshotName += "__" + label
        return snapshotName

    def getPartsFromName(self):
        laseDirName = os.path.basename(self.path)
        matchResult = re.match(r"^(.*?)__(.*?)(?:__(.*))?$", laseDirName)
        if matchResult:
            self.projectName = matchResult.group(1)
            timestamp = matchResult.group(2)
            try:
                timestamp = datetime.strptime(timestamp, timestampString)
            except ValueError:
                pass
            self.timestamp = timestamp
            if len(matchResult.groups()) > 2:
                self.label = matchResult.group(3)

        return None

    def getPath(self, filename: str = None):
        if filename is None:
            return self.path
        else:
            return self.path + "/" + filename

    def getTimestamp(self):
        return self.timestamp

    def hasFile(self, filename: str) -> bool:
        return os.path.exists(self.getPath(filename))

    def exists(self) -> bool:
        return os.path.exists(self.getPath())

    def delete(self):
        logging.warning("Deleting snapshot at {}".format(self.getPath()))
        return shutil.rmtree(self.getPath())

    def files(self):
        return os.listdir(self.path)

    def createDirectory(self):
        try:
            logging.debug("Creating directory at {}".format(self.getPath()))
            os.makedirs(self.getPath(), exist_ok=True)
        except:
            logging.warning("Failed to create directory %s", self.getPath())

    def __str__(self):
        return "<Snapshot {} {} {} exists={} files={}>".format(
            self.projectName,
            self.timestamp,
            self.label,
            self.exists(),
            len(self.files())
        )


class SnapshotManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def initSnapshot(self, projectName, label) -> Snapshot:
        snapshotName = Snapshot.nameFromParts(projectName, label=label)
        snapshot = Snapshot(self.config.getStashDir() + "/" + snapshotName)
        if not self.config.get('dry-run'):
            snapshot.createDirectory()
        return snapshot

    def getSnapshotByLabel(self, projectName: str, label: str) -> Snapshot:
        rootDirectory = self.config.getStashDir()
        for file in os.listdir(rootDirectory):
            if re.match(r'^{}__.*__{}$'.format(projectName, label), file) is not None:
                return Snapshot(rootDirectory + "/" + file)
        return None

    def getSnapshotByPath(self, path: str) -> Snapshot:
        return Snapshot(path)

    def getSnapshotsByProject(self, projectName: str) -> list:
        rootDirectory = self.config.getStashDir()
        snapshots = []
        for file in os.listdir(rootDirectory):
            if re.match(r'^{}__.*$'.format(projectName), file) is not None:
                snapshots.append(Snapshot(rootDirectory + "/" + file))
        return snapshots

    def deleteByPath(self, path: str):
        snapshot = self.getSnapshotByPath(path)
        if snapshot and snapshot.exists():
            snapshot.delete()

    def deleteByLabel(self, projectName: str, label: str):
        snpashot = self.getSnapshotByLabel(projectName, label)
        if snpashot and snpashot.exists():
            snpashot.delete()

    def deleteByProject(self, projectName: str):
        for snapshot in self.getSnapshotsByProject(projectName):
            if snapshot.exists():
                snapshot.delete()

    def getLatestSnapshot(self, projectName: str) -> Snapshot:
        snapshots = sorted(self.getSnapshotsByProject(projectName),
                           key=lambda s: s.getTimestamp(),
                           reverse=True)
        if len(snapshots) > 0:
            return snapshots[0]

    def getActiveSnapshotFor(self, projectName: str):
        if importLabel := self.config.get('label'):
            snapshot = self.getSnapshotByLabel(projectName, importLabel)
        elif importPath := self.config.get('path'):
            snapshot = self.getSnapshotByPath(importPath)
        else:
            snapshot = self.getLatestSnapshot(projectName)
        return snapshot
