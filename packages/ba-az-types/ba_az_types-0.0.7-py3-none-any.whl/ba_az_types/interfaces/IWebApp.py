from abc import ABCMeta, abstractmethod

from .ICategorizableResource import ICategorizableResource

class IWebApp(ICategorizableResource):
    __metaclass__ = ABCMeta
    
    APP_SERVICE_PLAN_KEY = "appServicePlan"
    """The key for the app service plan of the webapp in the definition JSON"""
    INSIGHTS_KEY = "insights"
    """The key for the insights of the webapp in the definition JSON"""

    @property
    @abstractmethod
    def app_service_plan(self) -> str:
        """The app service plan of the webapp"""
        pass
    
    @property
    @abstractmethod
    def insights(self) -> bool:
        """If insights is enabled for the webapp"""
        pass
    