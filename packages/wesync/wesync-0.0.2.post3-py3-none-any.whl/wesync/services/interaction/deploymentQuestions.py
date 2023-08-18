from wesync.services.interaction.userInteraction import UserInteraction


class DeploymentQuestions:

    def __init__(self, config):
        self.config = config
        self.userInteraction = UserInteraction()

    def chooseDeployment(self, projectName: str, prompt: str = None) -> str:
        deploymentChoices = [
            deployment.getName() for deployment in
            self.config.localConfigData.getDeploymentsForProject(projectName)
            ]

        if not prompt:
            prompt = "Choose deployment"
        prompt += " (" + ','.join(deploymentChoices) + ")"

        chosenDeploymentName = None
        while chosenDeploymentName not in deploymentChoices:
            chosenDeploymentName = self.userInteraction.askForAnswer(prompt)

        return chosenDeploymentName