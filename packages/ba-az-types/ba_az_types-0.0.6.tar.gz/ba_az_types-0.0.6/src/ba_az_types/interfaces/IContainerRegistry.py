from abc import ABCMeta, abstractmethod

from .ICategorizableResource import ICategorizableResource
from .IWebAppAssociatedResource import IWebAppAssociatedResource

class IContainerRegistry(ICategorizableResource, IWebAppAssociatedResource):
    """An abstract class that defines properties for any kind of Azure Container Registry"""

    __metaclass__ = ABCMeta