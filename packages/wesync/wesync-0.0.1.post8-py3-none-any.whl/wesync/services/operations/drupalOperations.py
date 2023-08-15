import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from wesync.services.snapshot import Snapshot


class DrupalOperationsService(ProjectOperationsService):

    drush = None
    baseCommand = []

    def __init__(self, *args, **kwargs):
        super(DrupalOperationsService, self).__init__(*args, **kwargs)
        self.detectDrush()

    def detectDrush(self, path: str = "vendor/drush/drush/drush"):
        if path:
            if self.pathExists(path):
                self.drush = path

        for testBinary in ["drush"]:
            if self.commandAvailable(testBinary):
                self.drush = testBinary
                break

        if self.drush:
            self.baseCommand = [self.drush, "--yes", "--root={}".format(self.deployment.get('path'))]
        else:
            raise RuntimeError("Failed to find drush command")

    def fullExport(self, snapshot: Snapshot):
        if self.artifactsConfig is None:
            self.exportDrupalFiles(snapshot.getPath('files.tar.gz'))
        else:
            self.exportArtifacts(snapshot)
        self.exportDatabase(snapshot.getPath('database.sql'))

    def fullImport(self, snapshot: Snapshot):
        if self.artifactsConfig is None:
            self.importDrupalFiles(snapshot.getPath('files.tar.gz'))
        else:
            self.importArtifacts(snapshot)
        self.importDatabase(snapshot.getPath('database.sql'))

    def exportDatabase(self, databaseExportFile):
        logging.info("Dumping Drupal database at {} to {}".format(self.deployment.getPath(), databaseExportFile))
        args = ["sql:dump", "--extra-dump='--add-drop-table --set-gtid-purged=OFF --no-tablespaces --single-transaction=false'",
                "--result-file={}".format(databaseExportFile)
                ]
        self.runDrush(args)

    def importDatabase(self, databaseImportFile):
        logging.info("Importing Drupal database at {} to {}".format(databaseImportFile, self.deployment.getPath()))
        args = ["sql-cli < {}".format(databaseImportFile)]
        self.runCommand(args, shell=True)

    def exportDrupalFiles(self, archiveExportFile):
        exportRootDir = self.deployment.getPath() + "/web/sites/default"
        self.archiveFiles(rootPath=exportRootDir, files=['files'], outputArchiveFile=archiveExportFile)

    def importDrupalFiles(self, archiveImportFile):
        importRootDir = self.deployment.getPath() + "/web/sites/default"
        self.unarchiveFiles(inputArchiveFile=archiveImportFile, rootPath=importRootDir, files=["files"], delete=True)

    def runDrush(self, args: list, **kwargs):
        return self.runCommand(self.baseCommand + args, **kwargs)
