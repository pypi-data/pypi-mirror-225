
class HasProcessors(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processors = []

    def getProcessors(self) -> list:
        return self.processors

    def addProcessor(self, processor):
        self.processors.append(processor)
