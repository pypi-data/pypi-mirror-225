from typing import Any

from .interfaces.IAzureResources import IAzureResources
from .interfaces.IWebApp import IWebApp

from .ResourceGroup import ResourceGroup

class WebApp(IWebApp):
    """Represents a webapp in Azure"""

    def __init__(self, definition_json: dict[str, Any], azure_resources: IAzureResources, category_name: str | None = None):
        self.__definition_json = definition_json
        
        self.__name = str(definition_json[self.NAME_KEY])
        self.__resource_group = self.__get_resource_group(definition_json, azure_resources)
        self.__category_name = category_name
        self.__app_service_plan = str(definition_json[self.APP_SERVICE_PLAN_KEY])
        self.__insights = bool(definition_json[self.INSIGHTS_KEY])
    
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

        resource_group: ResourceGroup | None = azure_resources.get_resource_group(str(definition_json[self.RESOURCE_GROUP_KEY])) # type: ignore

        if resource_group is None:
            raise Exception(f"Resource group {str(definition_json[self.RESOURCE_GROUP_KEY])} not found")

        return resource_group

    @property
    def name(self) -> str:
        """The name of the webapp"""

        return self.__name
    
    @property
    def resource_group(self) -> ResourceGroup:
        """The resource group of the webapp"""

        return self.__resource_group
    
    @property
    def category_name(self) -> str | None:
        """The category name of the webapp"""

        return self.__category_name

    @property
    def app_service_plan(self) -> str:
        """The app service plan of the webapp"""

        return self.__app_service_plan
    
    @property
    def insights(self) -> bool:
        """If insights is enabled for the webapp"""

        return self.__insights
    
    def to_json(self) -> dict[str, Any]:
        return {
            self.NAME_KEY: self.name,
            self.RESOURCE_GROUP_KEY: self.resource_group.name,
            self.APP_SERVICE_PLAN_KEY: self.app_service_plan,
            self.INSIGHTS_KEY: self.insights
        }