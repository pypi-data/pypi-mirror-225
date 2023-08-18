from typing import Any

from .interfaces.IStorageContainer import IStorageContainer
from .interfaces.IVarNameStorageContainer import IVarNameStorageContainer
from .interfaces.IStorageAccount import IStorageAccount

from .VarName import VarName

class StorageContainer(IStorageContainer, IVarNameStorageContainer):
    def __init__(self, definition_json: dict[str, Any], account: IStorageAccount):
        self.__definition_json = definition_json

        self.__category = account.category

        self.__name = str(definition_json[self.NAME_KEY])
        self.__account = account
        self.__var_name = VarName(definition_json[self.VAR_NAME_KEY])
    
    @property
    def category(self) -> str | None:
        """The BA infrastructure category of the storage container"""

        return self.__category

    @property
    def name(self) -> str:
        """The name of the storage container"""
        
        return self.__name
    
    @property
    def account(self) -> IStorageAccount:
        """The storage account the storage container is in"""
        
        return self.__account
    
    @property
    def var_name_object(self) -> VarName:
        """The variable name (object) for the storage container"""
        return self.__var_name
    
    @property
    def var_name(self) -> str:
        """The variable name for the storage container"""
        return self.__var_name.get(self).upper()
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name,
            self.VAR_NAME_KEY: self.var_name_object.to_json()
        }