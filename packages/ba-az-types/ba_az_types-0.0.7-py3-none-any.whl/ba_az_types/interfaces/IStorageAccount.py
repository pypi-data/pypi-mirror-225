from abc import ABCMeta, abstractmethod

from .ICategorizableResource import ICategorizableResource
from .IWebAppAssociatedResource import IWebAppAssociatedResource
from .IStorageContainer import IStorageContainer
from .IStorageTable import IStorageTable

class IStorageAccount(ICategorizableResource, IWebAppAssociatedResource):
    """An abstract representation of the internal representation of an Azure Storage Account"""

    __metaclass__ = ABCMeta
    
    CONTAINERS_KEY = "containers"
    """The key for the containers of the storage account in the definition JSON"""
    TABLES_KEY = "tables"
    """The key for the tables of the storage account in the definition JSON"""

    @property
    @abstractmethod
    def key(self) -> str:
        """The key of the storage account
        
        Note, this comes from a seperate "storage accounts" file rather than the "resources" file
        """

        pass
    @key.setter
    @abstractmethod
    def key(self, value: str):
        pass
    
    @property
    @abstractmethod
    def connection_string(self) -> str:
        """The connection string for the storage account
        
        Note, this comes from a separate "storage accounts" file rather than the "resources" file
        """

        pass
    @connection_string.setter
    @abstractmethod    
    def connection_string(self, value: str):
        pass

    @property
    @abstractmethod
    def containers(self) -> list[IStorageContainer]:
        """The containers in the storage account"""
        
        pass
    @abstractmethod
    def add_container(self, container: IStorageContainer):
        """Add a container to the storage account

        Args:
            container (IStorageContainer): The storage container to add
        """

        pass
    @abstractmethod
    def has_container(self, container_name: str) -> bool:
        """Check if a container exists in the storage account

        Args:
            container_name (str): The name of the container

        Returns:
            bool: True if the container exists, False otherwise
        """

        pass
    @abstractmethod
    def get_container(self, container_name: str) -> IStorageContainer | None:
        """Get a container from the storage account

        Args:
            container_name (str): The name of the container

        Returns:
            IStorageContainer: The storage container
        """

        pass
    @abstractmethod
    def remove_container(self, container: IStorageContainer):
        """Remove a container from the storage account

        Args:
            container (IStorageContainer): The storage container to remove
        """

        pass

    @property
    @abstractmethod
    def tables(self) -> list[IStorageTable]:
        """The tables in the storage account"""
        
        pass
    @abstractmethod
    def add_table(self, table: IStorageTable):
        """Add a table to the storage account

        Args:
            table (IStorageTable): The storage table to add
        """

        pass
    @abstractmethod
    def has_table(self, table_name: str) -> bool:
        """Check if a table exists in the storage account

        Args:
            table_name (str): The name of the table

        Returns:
            bool: True if the table exists, False otherwise
        """

        pass
    @abstractmethod
    def get_table(self, table_name: str) -> IStorageTable | None:
        """Get a table from the storage account

        Args:
            table_name (str): The name of the table

        Returns:
            IStorageTable: The storage table
        """

        pass
    @abstractmethod
    def remove_table(self, table: IStorageTable):
        """Remove a table from the storage account

        Args:
            table (IStorageTable): The storage table to remove
        """

        pass