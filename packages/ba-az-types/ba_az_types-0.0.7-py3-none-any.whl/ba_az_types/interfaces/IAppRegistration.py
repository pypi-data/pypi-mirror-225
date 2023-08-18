from abc import ABCMeta, abstractmethod

class IAppRegistration:
    __metaclass__ = ABCMeta

    NAME_KEY = "name"
    """The key for the name of the app registration in the definition JSON"""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the app registration"""
        pass

    @property
    @abstractmethod
    def app_id(self) -> str:
        """The app id of the app registration"""
        pass

    @app_id.setter
    @abstractmethod
    def app_id(self, value: str):
        pass

    @property
    @abstractmethod
    def app_secret(self) -> str:
        """The app secret of associated with the app registration"""
        pass

    @app_secret.setter
    @abstractmethod
    def app_secret(self, value: str):
        pass

    @property
    @abstractmethod
    def service_principal_id(self) -> str:
        """The id of the ervice principal associated with the app registration"""
        pass

    @service_principal_id.setter
    @abstractmethod
    def service_principal_id(self, value: str):
        pass