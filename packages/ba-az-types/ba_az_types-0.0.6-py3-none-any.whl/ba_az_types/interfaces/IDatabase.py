from abc import ABCMeta, abstractmethod

from .ICategorizableResource import ICategorizableResource
from .IWebAppAssociatedResource import IWebAppAssociatedResource

class IDatabase(ICategorizableResource, IWebAppAssociatedResource):
    """An abstract class that defines properties for any kind of Azure managed database"""

    __metaclass__ = ABCMeta

    