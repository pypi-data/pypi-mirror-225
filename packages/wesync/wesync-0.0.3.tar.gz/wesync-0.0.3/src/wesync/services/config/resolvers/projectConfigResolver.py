import os


class ProjectConfigResolver:

    projectDefaultDirectory = "/var/www"

    def __init__(self, **kwargs):
        self.path = None
        self.name = None
        self.type = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def resolveKey(self, key: str):
        methodName = 'resolve' + key.capitalize()
        method = getattr(self, methodName, None)
        if callable(method):
            return method()

    def resolvePath(self) -> str:
        if self.name:
            self.path = self.projectDefaultDirectory + "/" + self.name
        else:
            self.path = os.getcwd()
        return self.path

    def resolveName(self) -> str:
        path = self.path or os.getcwd()
        if path and '/var/www/' in path:
            pathStripped = path.replace('/var/www/', '')
            self.name = pathStripped.split('/')[0]

        return self.name

    def resolveType(self) -> str:
        if self.path:
            if os.path.exists(self.path + '/wp-config.php'):
                self.type = 'wordpress'
            elif os.path.exists(self.path + '/wp-includes'):
                self.type = 'wordpress'

            elif os.path.exists(self.path + '/web'):
                self.type = 'drupal'
            elif os.path.exists(self.path + '/sites'):
                self.type = 'drupal'

        return self.type
