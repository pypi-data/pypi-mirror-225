import os, re

from typing import Any

from .interfaces.IVarName import IVarName
from .interfaces.IVarNameStorageTable import IVarNameStorageTable
from .interfaces.IVarNameStorageContainer import IVarNameStorageContainer

class VarName(IVarName):
    CATEGORY_PREFIX_KEY = 'prefixCategoryName'
    """The key/property name for whether or not to prefix the category name (if the VarName is a dictionary instead of a string)"""
    REPLACE_KEY = 'replace'
    """The key/property name for the replace property (if the VarName is a dictionary instead of a string)"""
    SUFFIX_KEY = 'suffix'
    """The key/property name for the suffix property (if the VarName is a dictionary instead of a string)"""

    def __init__(self, value: str | dict[str, Any]):
        # If the value is a dictionary and it includes the category prefix property/key, we want to convert from a string to a proper boolean
        if type(value) == dict and self.CATEGORY_PREFIX_KEY in value:
            if value[self.CATEGORY_PREFIX_KEY].lower() == 'true':
                value[self.CATEGORY_PREFIX_KEY] = True
            elif value[self.CATEGORY_PREFIX_KEY].lower() == 'false':
                value[self.CATEGORY_PREFIX_KEY] = False
        
        self.value = value
    
    def handle_category_prefix(self, var_name_props: dict[str, Any], category_name: str) -> str:
        if self.CATEGORY_PREFIX_KEY in var_name_props:
            # Print debugging output if DEBUG_MODE is set
            if os.getenv('DEBUG_MODE') != None:
                print('The prefix property of the varName property was set')

            # Note, we only want to prefix if it's set to true
            if var_name_props[self.CATEGORY_PREFIX_KEY] == True:
                # Print debugging output if DEBUG_MODE is set
                if os.getenv('DEBUG_MODE') != None:
                    print('The prefix property of the varName property was set to true')

                return category_name
            else:
                return ''
        else:
            # Print debugging output if DEBUG_MODE is set
            if os.getenv('DEBUG_MODE') != None:
                print('The prefix property of the varName property was not set defaulting...');

            # Because the prefixCategoryName property isn't set default to prefixing the category name
            return category_name
    
    def handle_replacements(self, var_name_props: dict[str, Any], var_name_so_far: str) -> str:
        """Perform the replacements specified in the variable name's property to the encapsulating object's name

        Args:
            var_name_props (dict): The variable name's properties (where the replacements would be set, if set)
            var_name_so_far (str): The variable name so far (the name of the encapsulating object with any prefixes if set)

        Returns:
            str: The variable name with replacements filled in, if set. Otherwise the variable name as is
        """

        if self.REPLACE_KEY in var_name_props and len(var_name_props[self.REPLACE_KEY]) > 0:
            # Print debugging output if DEBUG_MODE is set
            if os.getenv('DEBUG_MODE') != None:
                print('The replace property is set on the varName property object')

            # Variable to hold the results of the replacements as we go
            name_with_replacements = var_name_so_far

            # Loop over the desired replacements and "calculate" the output
            for search_str in var_name_props[self.REPLACE_KEY]:
                # Print debugging output if DEBUG_MODE is set
                if os.getenv('DEBUG_MODE') != None:
                    print(f'Attempting to replace {search_str} with {var_name_props[self.REPLACE_KEY][search_str]} in {name_with_replacements}')

                # Actually do the replacements
                name_with_replacements = name_with_replacements.replace(search_str, var_name_props[self.REPLACE_KEY][search_str])

                # Print debugging output if DEBUG_MODE is set
                if os.getenv('DEBUG_MODE') != None:
                    print(f'After replacement {name_with_replacements}')

            # append the name with replacements to the actual full environment variable name being created
            return name_with_replacements
        else:
            # Because no replacements were specified simply use the name of the encapsulating object
            return var_name_so_far

    def handle_suffix(self, var_name_props: dict[str, Any], var_name_so_far: str) -> str:
        """Provide the suffix if set

        Args:
            var_name_props (dict): The variable name properties (where the suffix would be set, if set)
            encapsulating_obj (dict): The encapsulating object (the object the variable name is for)

        Returns:
            str: The suffix to use, if set. Otherwise an empty string
        """

        # Append the suffix if set
        if self.SUFFIX_KEY in var_name_props:
            suffix = var_name_props[self.SUFFIX_KEY]
            
            # Print debugging output if DEBUG_MODE is set
            if os.getenv('DEBUG_MODE') != None:
                print(f'Adding suffix: ${suffix}')
                    
            return var_name_props[self.SUFFIX_KEY]
        else:
            return ''
    
    def handle_dictionary_value(self, var_name_props: dict[str, Any], encapsulating_obj: IVarNameStorageTable | IVarNameStorageContainer) -> str:
        env_var_name = ''

        # Print debugging output if DEBUG_MODE is set
        if os.getenv('DEBUG_MODE') != None:
            print('The varName property was an object')
                    
        # Prefix the category name if the setting isn't set (default) or if it is set, but is set to true
        # That is, ONLY if the `prefixCategoryName` property is set to false do we not prefix the category name
        # This is an attempt to keep environment variable names as unique as possible (as we end up with quite a few)
        env_var_name += self.handle_category_prefix(var_name_props, str(encapsulating_obj.category))

        # Append the encapsulating object's name
        env_var_name += encapsulating_obj.name

        # Handle the replacements if set
        # 
        # Note, we do assignment here instead of appending because we want to replace the existing (which would be the 
        # encapsulating object's name prefixed with the category. Unless the `prefixCategoryName` was explicitly set to false, 
        # in which case it's just the encapsulating object's name) with the replaced version 
        # 
        # If no replacements are set this will simply return the env_var_name as is
        env_var_name = self.handle_replacements(var_name_props, env_var_name)

        # Handle the suffix if set
        env_var_name += self.handle_suffix(var_name_props, env_var_name)

        # Convert from camelCase to snake_case
        env_var_name = re.sub(r'(?<!^)(?=[A-Z])', '_', env_var_name).lower()

        # Append an appropriate suffix based on the type of encapsulating object
        if isinstance(encapsulating_obj, IVarNameStorageTable):
            env_var_name += '_STORAGE_TABLE_NAME'
        elif isinstance(encapsulating_obj, IVarNameStorageContainer): # type: ignore
            env_var_name += '_CONTAINER_NAME'

        # Print debugging output if DEBUG_MODE is set
        if os.getenv('DEBUG_MODE') != None:
            print(f'End result of varName object processing: ${env_var_name}')
        
        return env_var_name
    
    def get(self, encapsulating_obj: IVarNameStorageTable | IVarNameStorageContainer) -> str:
        # Print debugging output if DEBUG_MODE is set
        if os.getenv('DEBUG_MODE') != None:
            print(f'The varName property was set to: {str(self.value)}')

        if not isinstance(self.value, str):
            return self.handle_dictionary_value(self.value, encapsulating_obj)
        else:
            # the varName property is a string literal so just use it as the environment variable name
            return self.value
    
    def to_json(self) -> str | dict[str, Any]:
        return self.value