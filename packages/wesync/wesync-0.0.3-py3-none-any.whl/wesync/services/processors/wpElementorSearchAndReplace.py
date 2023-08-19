import logging

from wesync.services.operations.wordpressOperations import WordpressOperationsService
from .processor import Processor, ProcessorResult


class WPElementorSearchAndReplace(Processor, WordpressOperationsService):

    names = ["search-and-replace", "wp-search-and-replace"]
    name = "wp-elementor-search-and-replace"
    projectTypes = ['wordpress']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, searchAndReplaceOld=None, searchAndReplaceNew=None, skipCheckPlugins=False, force=True,
                **kwargs) -> ProcessorResult:
        super(WPElementorSearchAndReplace, self).execute()

        searchAndReplaceArgs = self.resolveSearchAndReplace(
            searchAndReplaceOld=searchAndReplaceOld,
            searchAndReplaceNew=searchAndReplaceNew
        )
        if searchAndReplaceArgs is None:
            return ProcessorResult()

        if skipCheckPlugins is False:
            for pluginData in self.getPluginList():
                if pluginData.get('name') in ['elementor', 'elementor-pro']:
                    break
            else:
                logging.debug("Skipping {}. Elementor plugin was not found".format(self.name))
                return ProcessorResult()

        (searchAndReplaceOld, searchAndReplaceNew) = searchAndReplaceArgs

        args = ["elementor", "replace_urls", searchAndReplaceOld, searchAndReplaceNew]
        if force is True:
            args += ["--force"]

        logging.info("Running {}: {}".format(self.name, ' '.join(args)))
        commandResult = self.runWpCli(args)

        return ProcessorResult({
            "searchAndReplaceOld": searchAndReplaceOld,
            "searchAndReplaceNew": searchAndReplaceNew
        }, commandResult=commandResult)

