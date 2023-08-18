from abc import ABCMeta, abstractmethod

class IVarNameStorageContainer:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def category(self) -> str | None:
        """The BA infrastructure category of the storage container"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the storage container"""
        pass
    
    @property
    @abstractmethod
    def var_name(self) -> str:
        """The variable name for the storage container"""
        
        pass