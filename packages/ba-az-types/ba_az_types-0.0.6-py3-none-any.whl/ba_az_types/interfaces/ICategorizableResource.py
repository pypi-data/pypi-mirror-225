from abc import ABCMeta

from .IResource import IResource

class ICategorizableResource(IResource):
    """An abstract class that defines properties for any kind of resource that can have a BA infrastructure category"""

    __metaclass__ = ABCMeta

    @property
    def category(self) -> str | None:
        """The BA infrastructure category of the resource

        Returns:
            str | None: The BA infrastructure category of the resource (or None if not applicable)
        """
        
        return None