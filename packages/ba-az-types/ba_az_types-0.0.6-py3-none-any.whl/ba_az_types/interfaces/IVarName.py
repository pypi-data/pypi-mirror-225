from abc import ABCMeta, abstractmethod

from typing import Any

from .IVarNameStorageTable import IVarNameStorageTable
from .IVarNameStorageContainer import IVarNameStorageContainer

class IVarName:
    __metacalss__ = ABCMeta

    @abstractmethod
    def handle_category_prefix(self, var_name_props: dict[Any, Any], category_name: str) -> str:
        pass
    
    @abstractmethod
    def handle_replacements(self, var_name_props: dict[Any, Any], var_name_so_far: str) -> str:
        """Perform the replacements specified in the variable name's property to the encapsulating object's name

        Args:
            var_name_props (dict): The variable name's properties (where the replacements would be set, if set)
            var_name_so_far (str): The variable name so far (the name of the encapsulating object with any prefixes if set)

        Returns:
            str: The variable name with replacements filled in, if set. Otherwise the variable name as is
        """
        pass

    @abstractmethod
    def handle_suffix(self, var_name_props: dict[Any, Any], var_name_so_far: str) -> str:
        """Provide the suffix if set

        Args:
            var_name_props (dict): The variable name properties (where the suffix would be set, if set)
            encapsulating_obj (dict): The encapsulating object (the object the variable name is for)

        Returns:
            str: The suffix to use, if set. Otherwise an empty string
        """
        pass
    
    @abstractmethod
    def handle_dictionary_value(self, var_name_props: dict[Any, Any], encapsulating_obj: IVarNameStorageTable | IVarNameStorageContainer) -> str:
        pass
    
    @abstractmethod
    def get(self, encapsulating_obj: IVarNameStorageTable | IVarNameStorageContainer) -> str:
        pass