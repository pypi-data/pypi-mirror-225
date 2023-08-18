from abc import ABCMeta, abstractmethod

from .IVarName import IVarName

class IStorageTable:
    """An abstract representation of the internal representation of an Azure Storage Table"""
    
    __metaclass__ = ABCMeta
    
    NAME_KEY = "name"
    """The key for the name of the storage table in the definition JSON"""
    VAR_NAME_KEY = "varName"
    """The key for the variable name of the storage table in the definition JSON"""
    DATA_KEY = "data"
    """The key for the data of the storage table in the definition JSON"""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the storage table"""
        
        pass

    @property
    @abstractmethod
    def var_name_object(self) -> IVarName:
        """The variable name (object) for the storage table"""
        
        pass
    
    @property
    @abstractmethod
    def var_name(self) -> str:
        """The variable name for the storage table"""
        
        pass

    @property
    @abstractmethod
    def data(self) -> list[dict[str, str]]:
        """The initial data of the storage table"""
        
        pass