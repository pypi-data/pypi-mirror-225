from abc import ABCMeta, abstractmethod

from .IVarName import IVarName

class IStorageContainer:
    """An abstract representation of the internal representation of an Azure Storage Container"""

    __metaclass__ = ABCMeta
    
    NAME_KEY = "name"
    """The key for the name of the storage container in the definition JSON"""
    VAR_NAME_KEY = "varName"
    """The key for the variable name of the storage container in the definition JSON"""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the storage container"""

        pass
    
    @property
    @abstractmethod
    def var_name_object(self) -> IVarName:
        """The variable name (object) for the storage container"""

        pass
    
    @property
    @abstractmethod
    def var_name(self) -> str:
        """The variable name for the storage container"""

        pass