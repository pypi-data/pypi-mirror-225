from wesync.services.config.sections.configData import SectionConfigData
from wesync.services.config.sections.projectConfig import ProjectConfigData


class ProcessorConfigData(SectionConfigData):

    mandatoryKeys = ['name']
    optionalKeys = '*'

    def __init__(self, project: ProjectConfigData, trigger: str):
        super(ProcessorConfigData, self).__init__()
        self.project = project
        self.trigger = trigger

    def getProject(self):
        return self.project

    def getTrigger(self):
        return self.trigger

    def getName(self):
        return self.get('name')

    def __str__(self):
        return str(self.data)

