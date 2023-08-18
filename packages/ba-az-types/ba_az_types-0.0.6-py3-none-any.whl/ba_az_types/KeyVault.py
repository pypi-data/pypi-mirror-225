from typing import Any

from .interfaces.IKeyVault import IKeyVault
from .interfaces.IAzureResources import IAzureResources
from .ResourceGroup import ResourceGroup
from .WebApp import WebApp
from .AppRegistration import AppRegistration

class KeyVault(IKeyVault):
    def __init__(self, definition_json: dict[str, Any], azure_resources: IAzureResources, category_name: str | None = None):
        self.__definition_json = definition_json

        self.__category_name = category_name

        self.__name = definition_json[self.NAME_KEY]
        
        self.__access: list[AppRegistration] = []
        for app_with_access in definition_json[self.ACCESS_KEY]:
            app_registration: AppRegistration | None = azure_resources.get_app_registration(app_with_access) # type: ignore
            if app_registration is not None:
                self.__access.append(app_registration)
        
        self.__web_apps = self.__get_web_apps(definition_json, azure_resources)
        self.__resource_group = self.__get_resource_group(definition_json, azure_resources)
    
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
            web_app_rgs: list[ResourceGroup] = [web_app.resource_group for web_app in self.__web_apps]
            if len(web_app_rgs) == 1:
                resource_group = web_app_rgs[0]
        
        if resource_group is None:
            raise Exception(f"Could not find resource group for database {self.name}")
    
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

    @property
    def category(self) -> str | None:
        """The category containing the Key Vault"""
        
        return self.__category_name

    @property
    def name(self) -> str:
        """The name of the Key Vault"""
        
        return self.__name
    
    @property
    def access(self) -> list[AppRegistration]: # type: ignore
        """The App Registrations that have access to the Key Vault"""
        
        return self.__access

    def app_has_access(self, app_object_id: str) -> bool:
        """Check if an App Registration has access to this Key Vault

        Args:
            app_object_id (str): The App Registration's object ID

        Returns:
            bool: True if the App Registration has access, False otherwise
        """

        for app in self.__access:
            if app.app_id == app_object_id:
                return True
        
        return False

    @property
    def resource_group(self) -> ResourceGroup:
        """The resource group of the Key Vault"""
        
        return self.__resource_group
    
    @property
    def web_apps(self) -> list[WebApp]: # type: ignore
        """The WebApp that has access to the Key Vault"""
        
        return self.__web_apps
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name,
            self.ACCESS_KEY: [app.name for app in self.access],
            self.RESOURCE_GROUP_KEY: self.resource_group.name,
            self.WEB_APPS_KEY: [web_app.name for web_app in self.web_apps]
        }