from abc import ABCMeta, abstractmethod

from .IResourceGroup import IResourceGroup

class IResource:
    """An abstract class that defines properties for any kind of resource (namely their name and resource group)"""

    __metaclass__ = ABCMeta

    NAME_KEY = "name"
    """The key for the name of the resource in the definition JSON"""
    RESOURCE_GROUP_KEY = "resourceGroup"
    """The key for the resource group of the resource in the definition JSON"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def resource_group(self) -> IResourceGroup:
        pass