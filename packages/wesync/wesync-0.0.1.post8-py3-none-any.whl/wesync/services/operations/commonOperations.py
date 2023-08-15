import logging
from wesync.services.config.configManager import ConfigManager
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.execute.localCommandExecutor import LocalCommandExecutor
from wesync.services.execute.remoteCommandExecutor import RemoteCommandExecutor


class CommonOperationsService:

    def __init__(self, deployment: DeploymentConfigData, config: ConfigManager):
        self.config = config
        self.deployment = deployment
        self.artifactsConfig = self.deployment.getProject().getArtifacts()
        self.project = self.deployment.getProject()
        self.executor = self.getExecutor()

    def getExecutor(self):
        if self.deployment.isLocal() is True:
            return LocalCommandExecutor(self.config)
        else:
            return RemoteCommandExecutor(self.config, self.deployment)

    def runCommand(self, args, **kwargs):
        if self.config.dryRun() is True:
            logging.info("Dry run: {} ({})".format(args, kwargs))
            return

        logging.debug(' '.join(args))
        return self.executor.execute(args, **kwargs)

    def deletePath(self, path, recursive=False, force=False, ignoreErrors=False):
        args = ["rm"]
        if recursive is True:
            args += ["-r"]
        if force is True:
            args += ["-f"]
        args += [path]
        if ignoreErrors is True:
            self.runCommand(args, ignoreRC=True)
        else:
            self.runCommand(args)

    def createPath(self, path):
        args = ["mkdir", "-p", "-v", path]
        self.runCommand(args)

    def cloneRepository(self, repositoryURL: str, branch: str = 'master'):
        args = ['git', 'clone', repositoryURL, '--branch', branch]
        logging.info("Cloning repository into" % repositoryURL)
        self.runCommand(args, cwd=self.project.get('path'))

    def commandAvailable(self, command) -> bool:
        processResult = self.runCommand(["which", command], ignoreRC=True)
        return processResult.returncode == 0

    def pathExists(self, path: str, **kwargs) -> bool:
        processResult = self.runCommand(['ls', path], ignoreRC=True, **kwargs)
        return processResult.returncode == 0

    def archiveFiles(self, rootPath: str, files: list, outputArchiveFile: str, **kwargs):
        logging.info("Archiving files at {}/{} to {}".format(rootPath, ','.join(files), outputArchiveFile))
        args = ["tar", "-czf", outputArchiveFile, '-C', rootPath] + files
        self.runCommand(args, **kwargs)

    def unarchiveFiles(self, inputArchiveFile, rootPath: str, files: list, delete=False, **kwargs):
        logging.info("Decompressing files at {} to {}/{}".format(inputArchiveFile, rootPath, ','.join(files)))

        if delete is True:
            for file in files:
                deletePath = '/'.join([rootPath, file])
                logging.debug("Removing files at {}".format(deletePath))
                self.deletePath(deletePath, recursive=True)

        args = ["tar", "-xzf", inputArchiveFile, '-C', rootPath] + files
        self.runCommand(args, **kwargs)