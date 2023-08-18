from abc import ABCMeta, abstractmethod

from .ICategorizableResource import ICategorizableResource
from .IWebAppAssociatedResource import IWebAppAssociatedResource

class IRedisCache(ICategorizableResource, IWebAppAssociatedResource):
    """An abstract class that defines properties for any kind of Azure Redis Cache"""

    __metaclass__ = ABCMeta