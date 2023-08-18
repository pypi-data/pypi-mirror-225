from wesync.commands.commandManager import Command
from wesync import __about__


class VersionCommand(Command):

    requiresConfig = False
    commandName = 'version'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, **kwargs):
        print (__about__.__version__)