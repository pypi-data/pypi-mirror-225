from wesync.services.config.sections.processorConfig import ProcessorConfigData
from wesync.services.config.sections.deploymentConfig import DeploymentConfigData
from wesync.services.config.configManager import ConfigManager
from wesync.services.processors.processor import Processor, ProcessorResult
from .wpSearchAndReplace import WPSearchAndReplace
from .runShellCmd import RunShellCmd
from .wpElementorSearchAndReplace import WPElementorSearchAndReplace


class ProcessorList:
    def __init__(self):
        self.processors = []

    def append(self, processor: Processor):
        self.processors.append(processor)

    def executeAll(self, *args, **kwargs):
        for processor in self.processors:
            processorResult = processor.execute(*args, **kwargs)        #type: ProcessorResult
            kwargs.update(processorResult.newArguments)

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
            RunShellCmd,
            WPElementorSearchAndReplace
        ]

    def getProcessorClasses(self, processorConfig: ProcessorConfigData) -> list:
        processorClasses = []
        processorType = processorConfig.getName()
        projectType = processorConfig.getProject().getType()

        for processor in self.processors:
            if (
                    (processorType == processor.name or processorType in processor.names) and
                    ('*' in processor.projectTypes or projectType in processor.projectTypes)
            ):
                processorClasses.append(processor)
        return processorClasses

    def getProcessors(self,
                      processorConfig: ProcessorConfigData,
                      deployment: DeploymentConfigData,
                      config: ConfigManager
                      ) -> list:

        return list(map(
            lambda processorClass: processorClass(processorConfig=processorConfig, deployment=deployment, config=config),
            self.getProcessorClasses(processorConfig)
        ))

    def getProcessorsForDeployment(self, deployment: DeploymentConfigData) -> ProcessorList:
        processors = ProcessorList()
        for processorConfig in deployment.getAllProcessors():
            for processor in self.getProcessors(processorConfig, deployment, self.config):
                processors.append(processor)
        return processors

    def getForAnyTrigger(self, triggers: list, deployment: DeploymentConfigData):
        allProcessors = self.getProcessorsForDeployment(deployment)
        filteredProcessors = ProcessorList()
        for trigger in triggers:
            filteredProcessors += allProcessors.filterByTrigger(trigger)
        return filteredProcessors
