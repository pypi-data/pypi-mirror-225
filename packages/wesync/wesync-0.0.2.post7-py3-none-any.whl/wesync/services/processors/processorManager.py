from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.processors.processor import Processor
from .wpSearchAndReplace import WPSearchAndReplace
from .runShellCmd import RunShellCmd


class ProcessorList:
    def __init__(self):
        self.processors = []

    def append(self, processor: Processor):
        self.processors.append(processor)

    def executeAll(self, *args, **kwargs):
        for processor in self.processors:
            processor.execute(*args, **kwargs)

    def filterByTrigger(self, processorTrigger: str):
        newList = ProcessorList()
        for processor in self.processors:
            if processor.processorConfig.getTrigger() == processorTrigger:
                newList.append(processor)
        return newList

    def __iter__(self):
        return self.processors

    def __add__(self, other):
        addProcessorList = ProcessorList()
        for processor in self.processors + other.processors:
            if processor not in addProcessorList.processors:
                addProcessorList.append(processor)
        return addProcessorList


class ProcessorManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.processors = [
            WPSearchAndReplace,
            RunShellCmd
        ]

    def getProcessorClass(self, processorConfig: ProcessorConfigData):
        processorType = processorConfig.getName()
        projectType = processorConfig.getProject().getType()

        for processor in self.processors:
            if (
                    (processorType == processor.name or processorType in processor.names) and
                    ('*' in processor.projectTypes or projectType in processor.projectTypes)
            ):
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

    def getProcessorsForDeployment(self, deployment: DeploymentConfigData) -> ProcessorList:
        processors = ProcessorList()
        for processorConfig in deployment.getAllProcessors():
            processors.append(self.getProcessor(processorConfig, deployment, self.config))
        return processors

    def getForAnyTrigger(self, triggers: list, deployment: DeploymentConfigData):
        allProcessors = self.getProcessorsForDeployment(deployment)
        filteredProcessors = ProcessorList()
        for trigger in triggers:
            filteredProcessors += allProcessors.filterByTrigger(trigger)
        return filteredProcessors
