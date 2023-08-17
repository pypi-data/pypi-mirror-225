import logging
from wesync.services.interaction.userInteraction import UserInteraction


class Processor():

    name = "processor"

    def __init__(self):
        self.userInteraction = UserInteraction()

    def askForArgument(self, argument: str, **kwargs):
        return self.userInteraction.askForAnswer(self.name + " value for '" + argument + "'", **kwargs)

    def execute(self, *args, **kwargs):
        logging.info("Running " + self.name)
