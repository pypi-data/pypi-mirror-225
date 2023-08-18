from .terminal import bcolors


class UserInteraction:
    def __init__(self):
        pass

    def getColorForLevel(self, level: str):
        if level == 'info':
            return bcolors.OKCYAN
        if level == 'success':
            return bcolors.OKGREEN
        if level == 'warn':
            return bcolors.WARNING
        if level == 'fail':
            return bcolors.FAIL
        return bcolors.OKBLUE

    def askForAnswer(self, prompt: str, default=None, allowEmpty=False):
        while True:
            if default is None:
                value = input("{}: ".format(prompt))
            else:
                value = input("{} [{}]: ".format(prompt, default)) or default

            if value:
                return value

            if allowEmpty is True:
                return value

            else:
                print("Invalid input for previous prompt\n")

    def confirm(self, prompt: str = "Continue operation ?", default=False, level="info"):
        if default is True:
            choices = "Y/n"
        elif default is False:
            choices = "y/N"
        else:
            choices = "y/n"

        startColor = self.getColorForLevel(level)

        while True:
            try:
                value = input(startColor + "{} {}: ".format(prompt, choices) + bcolors.ENDC)
                if value in ["n", "N"]:
                    return False
                elif value in ["y", "Y"]:
                    return True
                elif not value:
                    if default is not None:
                        return default
                else:
                    print("Invalid input for previous prompt\n")

            except KeyboardInterrupt:
                return False