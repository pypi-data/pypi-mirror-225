import logging
import os
import re
from datetime import datetime, timedelta
from wesync.services.execute.localCommandExecutor import LocalCommandExecutor
from wesync.services.config.configManager import ConfigManager


class RemoteConfigService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.executor = LocalCommandExecutor(config)

    def hasConfigDirectory(self) -> bool:
        configDir = self.config.getConfigDir()
        result = self.executor.execute(["ls", "-d", configDir], ignoreRC=True)
        return result.returncode == 0

    def cloneConfigRepository(self):
        configdir = self.config.getConfigDir()
        if os.path.exists(configdir) and len(os.listdir(configdir)) == 0:
            configRepo = self.config.getConfigRepository()
            logging.info("Cloning config from {} into {}".format(configRepo, configdir))
            self.executor.execute(["git", "clone", configRepo, configdir])

    def getLastConfigUpdate(self):
        configdir = self.config.getConfigDir()
        gitFetchHeadFile = configdir + "/.git/FETCH_HEAD"

        result = self.executor.execute(["stat", "--format=\"Modify: %y\"", gitFetchHeadFile], ignoreRC=True)
        if result.returncode != 0:
            result = self.executor.execute(["stat", "-x", gitFetchHeadFile], ignoreRC=True)
            if result.returncode != 0:
                return None

        resultOutput = re.findall(r"Modify: ([\d-]+\s[\d:]+).*", result.stdout.decode())
        if not resultOutput:
            return None

        try:
            timestamp = datetime.strptime(resultOutput[0], "%Y-%m-%d %H:%M:%S")
        except:
            return None

        return timestamp

    def isConfigRepositoryOutdated(self) -> bool:
        if lastTimestamp := self.getLastConfigUpdate():
            return datetime.now() > lastTimestamp + timedelta(hours=24)
        else:
            return False

    def fetchConfigRepository(self, force=False):
        configdir = self.config.getConfigDir()
        if not self.isConfigRepositoryOutdated() and force is False:
            logging.debug("remoteConfig fetch not required")
            return

        if force is False:
            logging.info("Checking for remote changes for config")

        self.executor.execute(["git", "remote", "update"], cwd=configdir)

    def hasChangesInConfigRepository(self):
        configdir = self.config.getConfigDir()
        result = self.executor.execute(["git", "status"], cwd=configdir)
        resultOutput = result.stdout.decode()
        if re.findall(r"Your branch is up to date", resultOutput):
            return False

        if re.findall(r"and can be fast-forwarded", resultOutput):
            return True

        logging.warning("Unexpected git status output: {}".format(resultOutput))
        return None

    def pullConfigRepository(self):
        configdir = self.config.getConfigDir()
        logging.info("Fetching remote changes for config")
        self.executor.execute(["git", "pull"], cwd=configdir)

    def commitConfigRepository(self, commitMessage):
        configdir = self.config.getConfigDir()

        self.executor.execute(["git", "add", "."], cwd=configdir)
        logging.debug("Creating new commit")
        commitResult = self.executor.execute(["git", "commit", "-m", commitMessage], cwd=configdir, ignoreRC=True)

        if commitResult.returncode > 0:
            commitStdout = commitResult.stdout.decode()
            if "nothing to commit" in commitStdout:
                logging.info(commitStdout)
            else:
                raise RuntimeError("Failed to complete command git commit")

    def pushConfigRepository(self):
        configdir = self.config.getConfigDir()
        logging.debug("Pushing config repository")
        self.executor.execute(["git", "push"], cwd=configdir)
