from abc import ABCMeta, abstractmethod

from .IWebApp import IWebApp

class IWebAppAssociatedResource:
    """An abstract class that defines properties for resources that can be associated with a or a collection of webapp(s)"""

    __metaclass__ = ABCMeta

    WEB_APPS_KEY = "webApps"
    """The key for the associated web apps array of the resource in the definition JSON"""

    @property
    @abstractmethod
    def web_apps(self) -> list[IWebApp]:
        pass

    