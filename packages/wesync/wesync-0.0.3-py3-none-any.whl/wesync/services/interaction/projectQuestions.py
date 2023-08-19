from wesync.services.interaction.userInteraction import UserInteraction


class ProjectQuestions:

    def __init__(self, config):
        self.config = config
        self.userInteraction = UserInteraction()

    def chooseProject(self, prompt: str = None) -> str:
        projectChoices = [
            project.getName() for project in
            self.config.localConfigData.projects.values()
        ]

        if not prompt:
            prompt = "Choose project"

        prompt += " (" + ','.join(projectChoices) + ")"

        chosenProjectName = None
        while chosenProjectName not in projectChoices:
            chosenProjectName = self.userInteraction.askForAnswer(prompt)

        return chosenProjectName
