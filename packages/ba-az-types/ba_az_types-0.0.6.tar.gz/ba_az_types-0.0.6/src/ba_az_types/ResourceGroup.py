from typing import Any

from .interfaces.IResourceGroup import IResourceGroup

class ResourceGroup(IResourceGroup):
    """Represents a resource group in Azure
    
    Note, that properties are used with no setters. This is because the resource group definitions should not be changed.

    Attributes:
        name (str): The name of the resource group
    """

    def __init__(self, definition_json: dict[str, Any]):
        self.__definition_json = definition_json

        self.__name = definition_json[self.NAME_KEY]
    
    @property
    def name(self) -> str:
        """The name of the resource group"""
        
        return self.__name
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name
        }