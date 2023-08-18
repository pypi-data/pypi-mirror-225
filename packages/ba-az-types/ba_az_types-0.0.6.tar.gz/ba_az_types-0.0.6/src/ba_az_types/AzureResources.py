from typing import Any, Literal

from .interfaces.IAzureResources import IAzureResources

from .ResourceGroup import ResourceGroup
from .WebApp import WebApp
from .ContainerRegistry import ContainerRegistry
from .AppRegistration import AppRegistration
from .Database import Database
from .RedisCache import RedisCache
from .StorageAccount import StorageAccount
from .KeyVault import KeyVault

class AzureResources(IAzureResources):
    def __init__(self, definition_json: dict[str, Any]):
        self.__definition_json = definition_json
        
        # Create resource group objects from the definition JSON and store them in a list
        self.__resource_groups: list[ResourceGroup] = []
        for resource_group_definition in definition_json[IAzureResources.RESOURCE_GROUPS_KEY]:
            resource_group = ResourceGroup(resource_group_definition)
            self.__resource_groups.append(resource_group)
        
        # Create webapp objects from the definition JSON and store them in a list
        self.__web_apps: list[WebApp] = []
        for web_app_definition in definition_json[IAzureResources.WEB_APPS_KEY]:
            web_app = WebApp(web_app_definition, self)
            self.__web_apps.append(web_app)
        
        # Create container registry objects from the definition JSON and store them in a list
        self.__container_registries: list[ContainerRegistry] = []
        if IAzureResources.CONTAINER_REGISTRIES_KEY in definition_json:
            for container_registry_definition in definition_json[IAzureResources.CONTAINER_REGISTRIES_KEY]:
                container_registry = ContainerRegistry(container_registry_definition, self)
                self.__container_registries.append(container_registry)
        
        # Create app registration objects from the definition JSON and store them in a list
        self.__app_registrations: list[AppRegistration] = []
        if IAzureResources.APP_REGISTRATIONS_KEY in definition_json:
            for app_registration_definition in definition_json[IAzureResources.APP_REGISTRATIONS_KEY]:
                app_registration = AppRegistration(app_registration_definition)
                self.__app_registrations.append(app_registration)
        
        self.__databases: list[Database] = []
        if IAzureResources.DATABASES_KEY in definition_json:
            for database_definition in definition_json[IAzureResources.DATABASES_KEY]:
                database = Database(database_definition, self)
                self.__databases.append(database)
        
        self.__redis_caches: list[RedisCache] = []
        if IAzureResources.CACHES_KEY in definition_json:
            for redis_cache_definition in definition_json[IAzureResources.CACHES_KEY]:
                redis_cache = RedisCache(redis_cache_definition, self)
                self.__redis_caches.append(redis_cache)

        self.__storage_accounts: list[StorageAccount] = []
        if IAzureResources.STORAGE_KEY in definition_json:
            for storage_account_definition in definition_json[IAzureResources.STORAGE_KEY]:
                storage_account = StorageAccount(storage_account_definition, self)
                self.__storage_accounts.append(storage_account)
        
        self.__key_vaults: list[KeyVault] = []
        if IAzureResources.VAULTS_KEY in definition_json:
            for key_vault_definition in definition_json[IAzureResources.VAULTS_KEY]:
                key_vault = KeyVault(key_vault_definition, self)
                self.__key_vaults.append(key_vault)
        
        # Create categorized resources objects from the different category resources defined in the definition JSON and store 
        # them in a dictionary (by category name)
        self.__categorized_resources = self.__get_categorized_resources(definition_json)

    # =================
    # Internal Methods
    # =================

    def __get_categorized_resources(self, definition_json: dict[str, Any]) -> dict[str, list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp]]:
        """Gets the categorized resources from the definition JSON

        Args:
            definition_json (dict): The definition JSON

        Returns:
            dict[str, list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp]]: The categorized resources dictionary (by category name)
        """

        # Create categorized resources objects from the different category resources defined in the definition JSON and store 
        # them in a dictionary (by category name)
        categorized_resources: dict[str, list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp]] = {}

        if IAzureResources.CATEGORIZED_RESOURCES_KEY not in definition_json:
            return categorized_resources
        
        for category_name, category_resources_by_type in dict(definition_json[self.CATEGORIZED_RESOURCES_KEY]).items():
            # Variable to hold the list of resources for the current category
            category_resources: list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp] = []
            
            if IAzureResources.CONTAINER_REGISTRIES_KEY in category_resources_by_type:
                for container_registry_definition in category_resources_by_type[IAzureResources.CONTAINER_REGISTRIES_KEY]:
                    container_registry = ContainerRegistry(container_registry_definition, self, category_name)
                    category_resources.append(container_registry)
            
            if IAzureResources.DATABASES_KEY in category_resources_by_type:
                for database_definition in category_resources_by_type[IAzureResources.DATABASES_KEY]:
                    database = Database(database_definition, self, category_name)
                    category_resources.append(database)
            
            if IAzureResources.STORAGE_KEY in category_resources_by_type:
                for storage_account_definition in category_resources_by_type[IAzureResources.STORAGE_KEY]:
                    storage_account = StorageAccount(storage_account_definition, self, category_name)
                    category_resources.append(storage_account)
            
            if IAzureResources.VAULTS_KEY in category_resources_by_type:
                for key_vault_definition in category_resources_by_type[IAzureResources.VAULTS_KEY]:
                    key_vault = KeyVault(key_vault_definition, self, category_name)
                    category_resources.append(key_vault)
            
            if IAzureResources.CACHES_KEY in category_resources_by_type:
                for redis_cache_definition in category_resources_by_type[IAzureResources.CACHES_KEY]:
                    redis_cache = RedisCache(redis_cache_definition, self, category_name)
                    category_resources.append(redis_cache)
            
            if IAzureResources.WEB_APPS_KEY in category_resources_by_type:
                for web_app_definition in category_resources_by_type[IAzureResources.WEB_APPS_KEY]:
                    web_app = WebApp(web_app_definition, self, category_name)
                    category_resources.append(web_app)

            categorized_resources[category_name] = category_resources
        
        return categorized_resources

    # ================
    # Resource Groups
    # ================

    @property
    def resource_groups(self) -> list[ResourceGroup]: # type: ignore
        """The resource groups in the Azure Resources"""

        return self.__resource_groups
    
    def add_resource_group(self, resource_group: ResourceGroup):
        """Add a resource group to the Azure Resources

        Args:
            resource_group (ResourceGroup): The resource group to add
        """

        self.__resource_groups.append(resource_group)

    def has_resource_group(self, name: str) -> bool:
        """Check if the Azure Resources has a resource group with the specified name
        
        Args:
            name (str): The name of the resource group to check for
        
        Returns:
            bool: True if the Azure Resources has a resource group with the specified name, False otherwise
        """

        # Loop over each resource group in the Azure Resources and check if the name matches
        for resource_group in self.resource_groups:
            if resource_group.name == name:
                return True
        
        return False
    
    def get_resource_group(self, name: str) -> ResourceGroup | None:
        """Get the resource group with the specified name

        Args:
            name (str): The name of the resource group to get

        Returns:
            dict | None: The resource group with the specified name or None if it does not exist
        """
        
        if self.has_resource_group(name):
            for resource_group in self.resource_groups:
                if resource_group.name == name:
                    return resource_group
        
        return None
    
    # =========
    # Web Apps
    # =========

    @property
    def web_apps(self) -> list[WebApp]: # type: ignore
        """The web apps in the Azure Resources"""

        return self.__web_apps
    
    def add_web_app(self, web_app: WebApp): # type: ignore
        """Add a web app to the Azure Resources

        Args:
            web_app (WebApp): The web app to add
        """

        self.__web_apps.append(web_app)

    def has_web_app(self, name: str) -> bool:
        """Check if the Azure Resources has a web app with the specified name
        
        Args:
            name (str): The name of the web app to check for
        
        Returns:
            bool: True if the Azure Resources has a web app with the specified name, False otherwise
        """

        for web_app in self.web_apps:
            if web_app.name == name:
                return True
            
        return False
    
    def get_web_app(self, name: str) -> WebApp | None:
        """Get the web app with the specified name

        Args:
            name (str): The name of the web app to get

        Returns:
            dict | None: The web app with the specified name or None if it does not exist
        """
        
        if self.has_web_app(name):
            for web_app in self.web_apps:
                if web_app.name == name:
                    return web_app
        
        return None

    # =====================
    # Container Registries
    # =====================

    @property
    def container_registries(self) -> list[ContainerRegistry]: # type: ignore
        """The container registries in the Azure Resources"""

        return self.__container_registries
    
    def add_container_registry(self, container_registry: ContainerRegistry): # type: ignore
        """Add a container registry to the Azure Resources

        Args:
            container_registry (ContainerRegistry): The container registry to add
        """

        self.__container_registries.append(container_registry)

    def has_container_registry(self, name: str) -> bool:
        """Check if the Azure Resources has a container registry with the specified name
        
        Args:
            name (str): The name of the container registry to check for
        
        Returns:
            bool: True if the Azure Resources has a container registry with the specified name, False otherwise
        """

        for container_registry in self.container_registries:
            if container_registry.name == name:
                return True
            
        return False
    
    def get_container_registry(self, name: str) -> ContainerRegistry | None:
        """Get the container registry with the specified name

        Args:
            name (str): The name of the container registry to get

        Returns:
            dict | None: The container registry with the specified name or None if it does not exist
        """
        
        if self.has_container_registry(name):
            for container_registry in self.container_registries:
                if container_registry.name == name:
                    return container_registry
        
        return None
    
    # ==================
    # App Registrations
    # ==================

    @property
    def app_registrations(self) -> list[AppRegistration]: # type: ignore
        """The app registrations in the Azure Resources"""

        return self.__app_registrations
    
    def add_app_registration(self, app_registration: AppRegistration):
        """Add an app registration to the Azure Resources

        Args:
            app_registration (AppRegistration): The app registration to add
        """

        self.__app_registrations.append(app_registration)

    def has_app_registration(self, name: str) -> bool:
        """Check if the Azure Resources has an app registration with the specified name
        
        Args:
            name (str): The name of the app registration to check for
        
        Returns:
            bool: True if the Azure Resources has an app registration with the specified name, False otherwise
        """

        for app_registration in self.app_registrations:
            if app_registration.name == name:
                return True
            
        return False
    
    def get_app_registration(self, name: str) -> AppRegistration | None:
        """Get the app registration with the specified name

        Args:
            name (str): The name of the app registration to get

        Returns:
            dict | None: The app registration with the specified name or None if it does not exist
        """
        
        if self.has_app_registration(name):
            for app_registration in self.app_registrations:
                if app_registration.name == name:
                    return app_registration
        
        return None
    
    # ==========
    # Databases
    # ==========

    @property
    def databases(self) -> list[Database]: # type: ignore
        """The databases in the Azure Resources"""

        return self.__databases
    
    def add_database(self, database: Database): # type: ignore
        """Add a database to the Azure Resources

        Args:
            database (Database): The database to add
        """

        self.__databases.append(database)

    def has_database(self, name: str) -> bool:
        """Check if the Azure Resources has a database with the specified name
        
        Args:
            name (str): The name of the database to check for
        
        Returns:
            bool: True if the Azure Resources has a database with the specified name, False otherwise
        """

        for database in self.databases:
            if database.name == name:
                return True
            
        return False
    
    def get_database(self, name: str) -> Database | None:
        """Get the database with the specified name

        Args:
            name (str): The name of the database to get

        Returns:
            dict | None: The database with the specified name or None if it does not exist
        """
        
        if self.has_database(name):
            for database in self.databases:
                if database.name == name:
                    return database
        
        return None

    # =======
    # Caches
    # =======

    @property
    def caches(self) -> list[RedisCache]: # type: ignore
        """The caches in the Azure Resources"""

        return self.__redis_caches
    
    def add_cache(self, cache: RedisCache): # type: ignore
        """Add a cache to the Azure Resources

        Args:
            cache (RedisCache): The cache to add
        """

        self.__redis_caches.append(cache) 

    def has_cache(self, name: str) -> bool:
        """Check if the Azure Resources has a cache with the specified name
        
        Args:
            name (str): The name of the cache to check for
        
        Returns:
            bool: True if the Azure Resources has a cache with the specified name, False otherwise
        """

        for cache in self.caches:
            if cache.name == name:
                return True
            
        return False
    
    def get_cache(self, name: str) -> RedisCache | None:
        """Get the cache with the specified name

        Args:
            name (str): The name of the cache to get

        Returns:
            dict | None: The cache with the specified name or None if it does not exist
        """
        
        if self.has_cache(name):
            for cache in self.caches:
                if cache.name == name:
                    return cache
        
        return None
    
    # ===============================
    # Uncategorized Storage Accounts
    # ===============================

    @property
    def uncategorized_storage(self) -> list[StorageAccount]: # type: ignore
        """The uncategorized storage accounts in the Azure Resources"""

        return self.__storage_accounts
    
    def add_uncategorized_storage(self, storage: StorageAccount): # type: ignore
        """Add an uncategorized storage account to the Azure Resources

        Args:
            storage (StorageAccount): The uncategorized storage account to add
        """

        self.__storage_accounts.append(storage)

    def has_uncategorized_storage(self, name: str) -> bool:
        """Check if the Azure Resources has an uncategorized storage account with the specified name
        
        Args:
            name (str): The name of the uncategorized storage account to check for
        
        Returns:
            bool: True if the Azure Resources has an uncategorized storage account with the specified name, False otherwise
        """

        for storage in self.uncategorized_storage:
            if storage.name == name:
                return True
            
        return False
    
    def get_uncategorized_storage(self, name: str) -> StorageAccount | None:
        """Get the uncategorized storage account with the specified name

        Args:
            name (str): The name of the uncategorized storage account to get

        Returns:
            dict | None: The uncategorized storage account with the specified name or None if it does not exist
        """
        
        if self.has_uncategorized_storage(name):
            for storage in self.uncategorized_storage:
                if storage.name == name:
                    return storage
        
        return None
    
    # =========================
    # Uncategorized Key Vaults
    # =========================

    @property
    def uncategorized_vaults(self) -> list[KeyVault]: # type: ignore
        """The uncategorized key vaults in the Azure Resources"""

        return self.__key_vaults
    
    def add_uncategorized_vaults(self, vault: KeyVault): # type: ignore
        """Add the uncategorized key vault to the Azure Resources

        Args:
            vault (KeyVault): The uncategorized key vault to add to the Azure Resources
        """

        self.__key_vaults.append(vault)

    def has_uncategorized_vault(self, name: str) -> bool:
        """Check if the Azure Resources has an uncategorized key vault with the specified name
        
        Args:
            name (str): The name of the uncategorized key vault to check for
        
        Returns:
            bool: True if the Azure Resources has an uncategorized key vault with the specified name, False otherwise
        """

        for vault in self.uncategorized_vaults:
            if vault.name == name:
                return True
            
        return False
    
    def get_uncategorized_vault(self, name: str) -> KeyVault | None:
        """Get the uncategorized key vault with the specified name

        Args:
            name (str): The name of the uncategorized key vault to get

        Returns:
            dict | None: The uncategorized key vault with the specified name or None if it does not exist
        """
        
        if self.has_uncategorized_vault(name):
            for vault in self.uncategorized_vaults:
                if vault.name == name:
                    return vault
        
        return None

    # =====================================================
    # Categorized Resources (BA Infrastructure Categories)
    # =====================================================

    @property
    def categorized_resources(self) -> dict[str, list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp]]: # type: ignore
        """The categorized resources in the Azure Resources"""
        
        return self.__categorized_resources
    
    def add_categorized_resource(self, category: str, *resource: ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp): # type: ignore
        """Add a categorized resource to the Azure Resources

        Args:
            category (str): The category of the resource to add
            resource (ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp): The resource to add
        """

        if category not in self.categorized_resources:
            self.categorized_resources[category] = []
        
        for res in resource:
            self.categorized_resources[category].append(res)

    def get_resource_categories(self) -> list[str]:
        """Get the categories of the resources in the Azure Resources

        Returns:
            list[str]: The categories of the resources in the Azure Resources
        """

        return list(self.categorized_resources.keys())
    
    def has_resource_category(self, category: str) -> bool:
        """Check if the Azure Resources has a resource category with the specified name
        
        Args:
            category (str): The category of the resource to check for
        
        Returns:
            bool: True if the Azure Resources has a resource category with the specified name, False otherwise
        """

        return category in self.categorized_resources
    
    def get_category_resources(self, category: str, types: list[Literal['ContainerRegistry'] | Literal['Database'] | Literal['StorageAccount'] | Literal['KeyVault'] | Literal['RedisCache'] | Literal['WebApp']] = ['ContainerRegistry', 'Database', 'StorageAccount', 'KeyVault', 'RedisCache', 'WebApp']) -> list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp] | None: # type: ignore
        """Get the resources in the Azure Resources with the specified category
        
        Args:
            category (str): The category of the resources to get
            types (list['ContainerRegistry' | 'Database' | 'StorageAccount' | 'KeyVault' | 'RedisCache' | 'WebApp']): The types of resources to get (default: all types)
        
        Returns:
            CategorizedResources | None: The resources in the Azure Resources with the specified category or None if the category does not exist
        """

        if self.has_resource_category(category):
            category_resources = self.categorized_resources[category]
            return_category_resources: list[ContainerRegistry | Database | StorageAccount | KeyVault | RedisCache | WebApp] = []
            
            for resource in category_resources:
                if type(resource).__name__ in types:
                    return_category_resources.append(resource)
            
            return return_category_resources
        
        return None
    
    # ==============
    # Other methods
    # ==============

    def to_json(self) -> dict[str, Any]:
        output = {
            self.RESOURCE_GROUPS_KEY: [resource_group.to_json() for resource_group in self.resource_groups],
            self.WEB_APPS_KEY: [web_app.to_json() for web_app in self.web_apps],
            self.CONTAINER_REGISTRIES_KEY: [container_registry.to_json() for container_registry in self.container_registries],
            self.APP_REGISTRATIONS_KEY: [app_registration.to_json() for app_registration in self.app_registrations],
            self.DATABASES_KEY: [database.to_json() for database in self.databases],
            self.CACHES_KEY: [cache.to_json() for cache in self.caches],
            self.STORAGE_KEY: [storage_account.to_json() for storage_account in self.uncategorized_storage],
            self.VAULTS_KEY: [vault.to_json() for vault in self.uncategorized_vaults],
        }

        categorized_resources = {}
        for category in self.get_resource_categories():
            categorized_resources[category] = {}
            
            category_storage_accounts: list[StorageAccount] = self.get_category_resources(category, ['StorageAccount']) # type: ignore
            categorized_resources[category][self.STORAGE_KEY] = [categorized_storage_account.to_json() for categorized_storage_account in category_storage_accounts]

            category_vaults: list[KeyVault] = self.get_category_resources(category, ['KeyVault']) # type: ignore
            categorized_resources[category][self.VAULTS_KEY] = [categorized_vault.to_json() for categorized_vault in category_vaults]
        
        output[self.CATEGORIZED_RESOURCES_KEY] = categorized_resources # type: ignore

        return output