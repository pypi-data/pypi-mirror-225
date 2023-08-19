import logging

from wesync.services.operations.wordpressOperations import WordpressOperationsService
from .processor import Processor, ProcessorResult


class WPSearchAndReplace(Processor, WordpressOperationsService):

    names = ["search-and-replace"]
    name = "wp-search-and-replace"
    projectTypes = ['wordpress']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, searchAndReplaceOld=None, searchAndReplaceNew=None, searchAndReplaceTable=None, **kwargs) -> ProcessorResult:
        super(WPSearchAndReplace, self).execute()

        searchAndReplaceArgs = self.resolveSearchAndReplace(
            searchAndReplaceOld=searchAndReplaceOld,
            searchAndReplaceNew=searchAndReplaceNew
        )
        if searchAndReplaceArgs is None:
            return ProcessorResult()

        (searchAndReplaceOld, searchAndReplaceNew) = searchAndReplaceArgs

        args = ["search-replace", searchAndReplaceOld, searchAndReplaceNew]
        if searchAndReplaceTable:
            args += [searchAndReplaceTable]
        if self.config.dryRun():
            args += ["--dry-run"]

        logging.info("Running {}: {}".format(self.name, ' '.join(args)))
        commandResult = self.runWpCli(args)

        return ProcessorResult({
                "searchAndReplaceOld": searchAndReplaceOld,
                "searchAndReplaceNew": searchAndReplaceNew
             }, commandResult=commandResult)
