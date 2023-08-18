from abc import ABCMeta, abstractmethod

from .IAppRegistration import IAppRegistration
from .ICategorizableResource import ICategorizableResource
from .IWebAppAssociatedResource import IWebAppAssociatedResource

class IKeyVault(ICategorizableResource, IWebAppAssociatedResource):
    """An abstract class that defines properties for any kind of Azure Key Vault"""

    __metaclass__ = ABCMeta
    
    ACCESS_KEY = "access"
    """The key for the access property"""

    @property
    @abstractmethod
    def access(self) -> list[IAppRegistration]:
        """The App Registrations that have access to the Key Vault"""

        pass

    @abstractmethod
    def app_has_access(self, app_object_id: str) -> bool:
        """Check if an App Registration has access to this Key Vault

        Args:
            app_object_id (str): The App Registration's object ID

        Returns:
            bool: True if the App Registration has access, False otherwise
        """

        pass