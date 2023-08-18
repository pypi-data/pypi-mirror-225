from typing import Any

from .interfaces.IContainerRegistry import IContainerRegistry
from .interfaces.IAzureResources import IAzureResources

from .ResourceGroup import ResourceGroup
from .WebApp import WebApp

class ContainerRegistry(IContainerRegistry):
    def __init__(self, definition_json: dict[str, str | list[str]], azure_resources: IAzureResources, category_name: str | None = None):
        self.__definition_json = definition_json

        self.__name = str(definition_json[self.NAME_KEY])
        self.__resource_group: ResourceGroup | None = azure_resources.get_resource_group(str(definition_json[self.RESOURCE_GROUP_KEY])) # type: ignore
        self.__category = category_name
        
        self.__web_apps: list[WebApp] = []
        if self.WEB_APPS_KEY in definition_json:
            for web_app_definition in list(definition_json[self.WEB_APPS_KEY]):
                web_app: WebApp = azure_resources.get_web_app(web_app_definition) # type: ignore
                self.__web_apps.append(web_app)

    @property
    def name(self) -> str:
        """The name of the container registry"""

        return self.__name
    
    @property
    def resource_group(self) -> ResourceGroup | None: # type: ignore
        """The resource group the container registry is in"""
        
        return self.__resource_group
    
    @property
    def category(self) -> str | None:
        """The category the container registry is in"""
        
        return self.__category

    @property
    def web_apps(self) -> list[WebApp]: # type: ignore
        """The webapps that use the container registry"""
        
        return self.__web_apps
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name,
            self.RESOURCE_GROUP_KEY: self.resource_group.name if self.resource_group else None,
            self.WEB_APPS_KEY: [web_app.name for web_app in self.web_apps]
        }