import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from wesync.services.snapshot import Snapshot


class DrupalOperationsService(ProjectOperationsService):

    drush = None
    baseCommand = []

    defaultFilePathArtifacts = [{
        "name": "files.tar.gz",
        "path": "web/sites/default/files"
    }]

    def __init__(self, *args, **kwargs):
        super(DrupalOperationsService, self).__init__(*args, **kwargs)

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
        self.exportFileArtifacts(snapshot)
        self.exportDatabaseToFile(snapshot.getPath('database.sql'))

    def fullImport(self, snapshot: Snapshot):
        self.importFileArtifacts(snapshot)
        self.importDatabaseFromFile(snapshot.getPath('database.sql'))

    def exportDatabaseToFile(self, databaseExportFile):
        logging.info("Dumping Drupal database at {} to {}".format(self.deployment.getPath(), databaseExportFile))
        args = ["sql:dump", "--extra-dump='--add-drop-table --set-gtid-purged=OFF --no-tablespaces --single-transaction=false'",
                "--result-file={}".format(databaseExportFile)
                ]
        self.runDrush(args)

    def importDatabaseFromFile(self, databaseImportFile):
        logging.info("Importing Drupal database at {} to {}".format(databaseImportFile, self.deployment.getPath()))
        args = ["sql-cli < {}".format(databaseImportFile)]
        self.runCommand(args, shell=True)

    def exportDatabaseToStdout(self, **kwargs):
        args = ["sql:dump",
                "--extra-dump='--add-drop-table --set-gtid-purged=OFF --no-tablespaces --single-transaction=false'"
                ]
        self.runDrush(args, **kwargs)

    def importDatabaseFromStdin(self, **kwargs):
        args = ["sql-cli"]
        self.runCommand(args, **kwargs)

    def runDrush(self, args: list, **kwargs):
        if not self.baseCommand:
            self.detectDrush()
        return self.runCommand(self.baseCommand + args, **kwargs)
