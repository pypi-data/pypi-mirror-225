import logging

from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.operations.wordpressOperations import WordpressOperationsService
from .processor import Processor


class WPSearchAndReplace(WordpressOperationsService, Processor):

    names = ["search-and-replace"]
    name = "wp-search-and-replace"
    projectTypes = ['wordpress']

    def __init__(self, processorConfig: ProcessorConfigData, *args, **kwargs):
        self.processorConfig = processorConfig
        super().__init__(*args, **kwargs)
        Processor.__init__(self)

    def execute(self, searchAndReplaceOld=None, searchAndReplaceNew=None, searchAndReplaceTable=None):
        super(WPSearchAndReplace, self).execute()

        if searchAndReplaceOld is None:
            searchAndReplaceOld = self.processorConfig.get('old')
            if searchAndReplaceOld is None:
                searchAndReplaceOld = self.askForArgument('old', allowEmpty=True)

        if not searchAndReplaceOld:
            logging.warning("Skipping search-and-replace because one term is empty")
            return

        if searchAndReplaceNew is None:
            searchAndReplaceNew = self.deployment.get('hostname')
            if not searchAndReplaceNew:
                self.askForArgument('new', allowEmpty=True)

        if not searchAndReplaceNew:
            logging.warning("Skipping search-and-replace because one term is empty")
            return

        if searchAndReplaceOld == searchAndReplaceNew:
            logging.warning("Skipping search-and-replace because terms are the same")
            return

        args = ["search-replace", searchAndReplaceOld, searchAndReplaceNew]
        if searchAndReplaceTable:
            args += [searchAndReplaceTable]
        if self.config.dryRun():
            args += ["--dry-run"]

        self.runWpCli(args)

