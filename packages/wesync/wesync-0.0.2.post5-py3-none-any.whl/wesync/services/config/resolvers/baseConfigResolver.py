import os
from collections import defaultdict


class BaseConfigResolver:

    def __init__(self, **kwargs):
        self.data = kwargs

    def resolveKey(self, key: str):
        methodName = 'resolve' + key.capitalize()
        method = getattr(self, methodName, None)
        if callable(method):
            return method()

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        return value
