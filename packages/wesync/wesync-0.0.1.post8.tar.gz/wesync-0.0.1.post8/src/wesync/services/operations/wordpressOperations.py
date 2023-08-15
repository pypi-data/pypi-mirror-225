import logging
from wesync.services.operations.projectOperations import ProjectOperationsService
from wesync.services.snapshot import Snapshot


class WordpressOperationsService(ProjectOperationsService):

    wpcli = None
    baseCommand = []

    def __init__(self, *args, **kwargs):
        super(WordpressOperationsService, self).__init__(*args, **kwargs)
        self.detectWPCLI()
        if self.wpcli is None:
            raise Exception("wp cli could not be found")

    def detectWPCLI(self):
        for testBinary in ["wp", "wp-cli", "wpcli"]:
            processResult = self.runCommand(["which", testBinary], ignoreRC=True)
            if processResult.returncode == 0:
                self.wpcli = testBinary
                break

        self.baseCommand = [self.wpcli, "--allow-root", "--path={}".format(self.deployment.get('path'))]

    def fullExport(self, snapshot: Snapshot):
        if self.artifactsConfig is None:
            self.exportWordpressFiles(snapshot.getPath('files.tar.gz'))
        else:
            self.exportArtifacts(snapshot)
        self.exportDatabase(snapshot.getPath('database.sql'))

    def fullImport(self, snapshot: Snapshot):
        if self.artifactsConfig is None:
            self.importWordpressFiles(snapshot.getPath('files.tar.gz'))
        else:
            self.importArtifacts(snapshot)
        self.importDatabase(snapshot.getPath('database.sql'))

    def exportDatabase(self, databaseExportFile):
        logging.info("Dumping Wordpress database at {} to {}".format(self.deployment.getPath(), databaseExportFile))
        self.runWpCli(["db", "export", databaseExportFile, "--add-drop-table"])

    def importDatabase(self, databaseImportFile):
        logging.info("Importing Wordpress database at {} to {}".format(databaseImportFile, self.deployment.getPath()))
        self.runWpCli(["db", "import", databaseImportFile])

    def exportWordpressFiles(self, archiveExportFile):
        exportRootDir = self.deployment.getPath() + "/wp-content"
        self.archiveFiles(rootPath=exportRootDir, files=['uploads'], outputArchiveFile=archiveExportFile)

    def importWordpressFiles(self, archiveImportFile):
        importRootDir = self.deployment.getPath() + "/wp-content"
        self.unarchiveFiles(inputArchiveFile=archiveImportFile, rootPath=importRootDir, files=["uploads"], delete=True)

    def runWpCli(self, args: list, **kwargs):
        return self.runCommand(self.baseCommand + args, **kwargs)
