from typing import Any

from .interfaces.IStorageTable import IStorageTable
from .interfaces.IVarNameStorageTable import IVarNameStorageTable
from .interfaces.IStorageAccount import IStorageAccount

from .VarName import VarName

class StorageTable(IStorageTable, IVarNameStorageTable):
    def __init__(self, definition_json: dict[str, Any], account: IStorageAccount):
        self.__definition_json = definition_json

        self.__category = account.category

        self.__name = str(definition_json[self.NAME_KEY])
        self.__account = account
        self.__var_name = VarName(definition_json[self.VAR_NAME_KEY])
        self.__data: list[dict[str, str]] = definition_json[self.DATA_KEY] if self.DATA_KEY in definition_json else []

    @property
    def category(self) -> str | None:
        """The category of the storage table"""
        
        return self.__category
    
    @property
    def name(self) -> str:
        """The name of the storage table"""
        
        return self.__name
    
    @property
    def account(self) -> IStorageAccount:
        """The storage account the storage table is in"""
        
        return self.__account
    
    @property
    def var_name_object(self) -> VarName:
        """The variable name (object) for the storage table"""
        
        return self.__var_name
    
    @property
    def var_name(self) -> str:
        """The variable name for the storage table"""
        
        return self.__var_name.get(self).upper()
    
    @property
    def data(self) -> list[dict[str, str]]:
        return self.__data
    
    def to_json(self) -> dict[str, Any]:
        return_obj = {
            self.NAME_KEY: self.name,
            self.VAR_NAME_KEY: self.var_name_object.to_json()
        }

        if len(self.data) > 0:
            return_obj[self.DATA_KEY] = self.data
        
        return return_obj