from typing import Any

from .interfaces.IStorageAccount import IStorageAccount
from .interfaces.IAzureResources import IAzureResources

from .ResourceGroup import ResourceGroup
from .WebApp import WebApp
from .StorageContainer import StorageContainer
from .StorageTable import StorageTable

class StorageAccount(IStorageAccount):
    def __init__(self, definition_json: dict[str, Any], azure_resources: IAzureResources, category_name: str | None = None):
        self.__definition_json = definition_json

        self.__name = definition_json[self.NAME_KEY]
        self.__category_name = category_name
        self.__key = ''
        self.__connection_string = ''
        self.__web_apps = self.__get_web_apps(definition_json, azure_resources)
        self.__resource_group = self.__get_resource_group(definition_json, azure_resources)
        self.__containers = self.__get_containers(definition_json)
        self.__tables = self.__get_tables(definition_json)
    
    def __get_resource_group(self, definition_json: dict[str, Any], azure_resources: IAzureResources) -> ResourceGroup:
        """Gets the resource group from the definition json

        Args:
            definition_json (dict): The definition json
            azure_resources (IAzureResources): The azure resources (used to get the resource group)

        Raises:
            Exception: If the resource group is not found

        Returns:
            ResourceGroup: The resource group
        """

        resource_group: ResourceGroup | None = azure_resources.get_resource_group(definition_json[self.RESOURCE_GROUP_KEY]) if self.RESOURCE_GROUP_KEY in definition_json else None # type: ignore
        if resource_group is None and len(self.__web_apps) > 0:
            web_app_rgs: list[ResourceGroup] = [web_app.resource_group for web_app in self.__web_apps if web_app.resource_group]
            if len(web_app_rgs) == 1:
                resource_group = web_app_rgs[0]
        
        if resource_group is None:
            raise Exception(f"Could not find resource group for storage account {self.name}")
    
        return resource_group

    def __get_web_apps(self, definition_json: dict[str, Any], azure_resources: IAzureResources) -> list[WebApp]:
        """Gets the associated web apps from the definition json

        Args:
            definition_json (dict): The definition json
            azure_resources (IAzureResources): The azure resources (used to get the web apps)

        Returns:
            list[WebApp]: The list associated web apps
        """

        if self.WEB_APPS_KEY in definition_json and type(definition_json[self.WEB_APPS_KEY]) is list:
            web_apps: list[WebApp] = []
            
            for web_app in definition_json[self.WEB_APPS_KEY]:
                web_app_object: WebApp = azure_resources.get_web_app(str(web_app)) # type: ignore
                web_apps.append(web_app_object)
            
            return web_apps
        else:
            return []

    def __get_containers(self, definition_json: dict[str, Any]) -> list[StorageContainer]:
        """Gets the containers for this storage account from the definition json

        Args:
            definition_json (dict): The definition json

        Returns:
            list[StorageContainer]: The list associated containers
        """

        if self.CONTAINERS_KEY in definition_json and type(definition_json[self.CONTAINERS_KEY]) is list:
            containers: list[StorageContainer] = []
            
            for container_definition in definition_json[self.CONTAINERS_KEY]:
                container: StorageContainer = StorageContainer(container_definition, self)
                containers.append(container)
            
            return containers
        
        # If no containers are defined, return an empty list
        return []
    
    def __get_tables(self, definition_json: dict[str, Any]) -> list[StorageTable]:
        """Gets the tables for this storage account from the definition json

        Args:
            definition_json (dict): The definition json

        Returns:
            list[StorageTable]: The list associated tables
        """

        if self.TABLES_KEY in definition_json and type(definition_json[self.TABLES_KEY]) is list:
            tables: list[StorageTable] = []
            
            for table_definition in definition_json[self.TABLES_KEY]:
                table: StorageTable = StorageTable(table_definition, self)
                tables.append(table)
            
            return tables
        
        # If no tables are defined, return an empty list
        return []

    @property
    def name(self) -> str:
        """The name of the storage account"""

        return self.__name
    
    @property
    def resource_group(self) -> ResourceGroup:
        """The resource group of the storage account"""

        return self.__resource_group

    @property
    def web_apps(self) -> list[WebApp]: # type: ignore
        """The name of the webapp that uses this storage account"""

        return self.__web_apps
    
    @property
    def category(self) -> str | None:
        """The category of the storage account"""

        return self.__category_name

    @property
    def key(self) -> str:
        """The key of the storage account
        
        Note, this comes from a seperate "storage accounts" file rather than the "resources" file
        """
        return self.__key
    
    @key.setter
    def key(self, value: str):
        self.__key = value
    
    @property
    def connection_string(self) -> str:
        """The connection string for the storage account
        
        Note, this comes from a seperate "storage accounts" file rather than the "resources" file
        """
        return self.__connection_string
    
    @connection_string.setter
    def connection_string(self, value: str):
        self.__connection_string = value

    @property
    def containers(self) -> list[StorageContainer]: # type: ignore
        """The storage container for the storage account"""
        
        return self.__containers
    
    def add_container(self, container: StorageContainer): # type: ignore
        self.__containers.append(container)

    def has_container(self, container_name: str) -> bool:
        for container in self.containers:
            if container.name == container_name:
                return True
        
        return False
    
    def get_container(self, container_name: str) -> StorageContainer | None:
        for container in self.containers:
            if container.name == container_name:
                return container
        
        return None
    
    def remove_container(self, container: StorageContainer): # type: ignore
        for i in range(len(self.containers)):
            if self.containers[i].name == container.name:
                del self.containers[i]
                break
    
    @property
    def tables(self) -> list[StorageTable]: # type: ignore
        return self.__tables
    
    def add_table(self, table: StorageTable): # type: ignore
        self.__tables.append(table)

    def has_table(self, table_name: str) -> bool:
        for table in self.tables:
            if table.name == table_name:
                return True
        
        return False
    
    def get_table(self, table_name: str) -> StorageTable | None:
        for table in self.tables:
            if table.name == table_name:
                return table
        
        return None
    
    def remove_table(self, table: StorageTable): # type: ignore
        for i in range(len(self.tables)):
            if self.tables[i].name == table.name:
                del self.tables[i]
                break
    
    def to_json(self) -> dict[str, Any]:
        return_obj = {
            self.NAME_KEY: self.name,
            self.RESOURCE_GROUP_KEY: self.resource_group.name,
            self.WEB_APPS_KEY: [web_app.name for web_app in self.web_apps]
        }

        if self.key != '':
            return_obj["key"] = self.key
        
        if self.connection_string != '':
            return_obj["connectionString"] = self.connection_string
        
        if len(self.containers) > 0:
            return_obj[self.CONTAINERS_KEY] = [container.to_json() for container in self.containers]
        
        if len(self.tables) > 0:
            return_obj[self.TABLES_KEY] = [table.to_json() for table in self.tables]
        
        return return_obj