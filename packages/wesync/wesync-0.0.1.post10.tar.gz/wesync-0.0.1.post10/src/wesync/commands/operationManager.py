from argparse import ArgumentParser


class Operation:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError()

    @staticmethod
    def configureArguments(argumentParser: ArgumentParser):
        return argumentParser
