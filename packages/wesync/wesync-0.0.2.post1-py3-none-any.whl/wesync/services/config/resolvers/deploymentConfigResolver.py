import socket
from .baseConfigResolver import BaseConfigResolver
from wesync.services.helpers.network import getDefaultIP


class DeploymentConfigResolver(BaseConfigResolver):

    def __init__(self, projectData=None, **kwargs):
        super(DeploymentConfigResolver, self).__init__(**kwargs)
        self.projectData = projectData

    def withProjectData(self, projectData: dict):
        self.projectData = projectData

    def getProjectData(self, key: str, default=None):
        return self.projectData.get(key, default)

    def resolveName(self):
        if not self.get('name'):
            self.set('name', socket.gethostname())
        return self.get('name')

    def resolveHost(self):
        if not self.get('host)'):
            self.set('host', getDefaultIP())
        return self.get('host')

    def resolvePort(self) -> str:
        if not self.get('port'):
            self.set('port', "22")
        return self.get('port')

    def resolveUsername(self) -> str:
        if not self.get('username'):
            self.set('username', 'developer')
        return self.get('username')

    def resolvePath(self):
        if not self.get('path'):
            if projectPath := self.getProjectData('path'):
                self.set('path', projectPath)
        return self.get('path')

