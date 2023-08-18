from abc import ABCMeta, abstractmethod

class IResourceGroup:
    __metaclass__ = ABCMeta

    NAME_KEY = "name"
    """The key for the name of the resource group in the definition JSON"""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the resource group"""
        pass