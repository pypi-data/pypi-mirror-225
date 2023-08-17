import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from wesync.services.snapshot import Snapshot


class WordpressOperationsService(ProjectOperationsService):

    wpcli = None
    baseCommand = []

    defaultFilePathArtifacts = [{
        "name": "uploads.tar.gz",
        "path": "wp-content/uploads"
    }]

    def __init__(self, *args, **kwargs):
        super(WordpressOperationsService, self).__init__(*args, **kwargs)

    def detectWPCLI(self):
        for testBinary in ["wp", "wp-cli", "wpcli"]:
            processResult = self.runCommand(["which", testBinary], ignoreRC=True)
            if processResult.returncode == 0:
                self.wpcli = testBinary
                break
        if self.wpcli is None:
            raise Exception("wp cli could not be found")

        self.baseCommand = [self.wpcli, "--allow-root", "--path={}".format(self.deployment.get('path'))]

    def fullExport(self, snapshot: Snapshot):
        self.exportFileArtifacts(snapshot)
        self.exportDatabaseToFile(snapshot.getPath('database.sql'))

    def fullImport(self, snapshot: Snapshot):
        self.importFileArtifacts(snapshot)
        self.importDatabaseFromFile(snapshot.getPath('database.sql'))

    def exportDatabaseToFile(self, databaseExportFile, **kwargs):
        logging.info("Dumping Wordpress database at {} to {}".format(self.deployment.getPath(), databaseExportFile))
        return self.runWpCli(["db", "export", databaseExportFile, "--add-drop-table"], **kwargs)

    def importDatabaseFromFile(self, databaseImportFile, **kwargs):
        logging.info("Importing Wordpress database at {} to {}".format(databaseImportFile, self.deployment.getPath()))
        return self.runWpCli(["db", "import", databaseImportFile], **kwargs)

    def importDatabaseFromStdin(self, **kwargs):
        return self.runWpCli(["db", "import", "-"], **kwargs)

    def exportDatabaseToStdout(self, **kwargs):
        return self.runWpCli(["db", "export", "-"], **kwargs)

    def runWpCli(self, args: list, **kwargs):
        if not self.baseCommand:
            self.detectWPCLI()
        return self.runCommand(self.baseCommand + args, **kwargs)
