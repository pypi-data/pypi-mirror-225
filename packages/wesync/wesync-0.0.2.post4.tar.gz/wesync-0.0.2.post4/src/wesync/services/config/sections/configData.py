from wesync.services.interaction.userInteraction import UserInteraction


class SectionConfigData:
    mandatoryKeys = []
    optionalKeys = []

    def __init__(self):
        self.clean = True
        self.data = {}
        self.interaction = UserInteraction()

    def loadFromConfig(self, configSectionDict):
        for key in configSectionDict:
            if key in self.mandatoryKeys or self.optionalKeys == '*' or key in self.optionalKeys:
                self.set(key, configSectionDict[key])

    def set(self, key: str, value):
        self.data[key] = value
        self.clean = False

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def has(self, key: str) -> bool:
        return key in self.data

    def getData(self) -> dict:
        return self.data

    def isClean(self) -> bool:
        return self.clean

    def setKeyFromInput(self, key: str, default=None, promptPrefix: str = None):
        if promptPrefix is None:
            prompt = str(key)
        else:
            prompt = str(promptPrefix) + " " + str(key)
        value = self.interaction.askForAnswer(prompt, default)
        self.set(key, value)
        return value

