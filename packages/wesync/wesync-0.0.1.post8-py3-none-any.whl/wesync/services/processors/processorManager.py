from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.processors.processor import Processor
from .wpSearchAndReplace import WPSearchAndReplace


class ProcessorList:
    def __init__(self):
        self.processors = []

    def append(self, processor: Processor):
        self.processors.append(processor)

    def executeAll(self, *args, **kwargs):
        for processor in self.processors:
            processor.execute(*args, **kwargs)

    def __iter__(self):
        return self.processors


class ProcessorManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.processors = [
            WPSearchAndReplace
        ]

    def getProcessorClass(self, processorConfig: ProcessorConfigData):
        processorType = processorConfig.getName()
        projectType = processorConfig.getProject().getType()

        for processor in self.processors:
            if (processorType == processor.name or processorType in processor.names) and projectType in processor.projectTypes:
                return processor
        return None

    def getProcessor(self,
                     processorConfig: ProcessorConfigData,
                     deployment: DeploymentConfigData,
                     config: ConfigManager
                     ):
        processorClass = self.getProcessorClass(processorConfig)
        if not processorClass:
            raise Exception("Failed to find processor for config {}".format(processorConfig.getName(), processorConfig))
        return processorClass(processorConfig=processorConfig, deployment=deployment, config=config)

    def getImportProcessors(self, deployment: DeploymentConfigData) -> ProcessorList:
        processors = ProcessorList()
        project = deployment.getProject()
        for processorConfig in project.getProcessors():
            if processorConfig.getTrigger() == 'import':
                processors.append(self.getProcessor(processorConfig, deployment, self.config))
        return processors
