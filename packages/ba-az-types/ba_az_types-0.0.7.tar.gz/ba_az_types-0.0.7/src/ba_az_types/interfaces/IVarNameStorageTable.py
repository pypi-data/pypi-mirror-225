from abc import ABCMeta, abstractmethod

class IVarNameStorageTable:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def category(self) -> str | None:
        """The category of the storage table"""
        
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the storage table"""
        
        pass
    
    @property
    @abstractmethod
    def var_name(self) -> str:
        """The variable name for the storage table"""
        
        pass