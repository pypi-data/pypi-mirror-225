"""
    QuaO Project provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import abstractmethod, ABC

from ...enum.provider_type import ProviderType


class Provider(ABC):

    def __init__(self, provider_type: ProviderType):
        self.provider_type = provider_type

    @abstractmethod
    def get_backend(self, device_specification):
        """

        """
        pass

    @abstractmethod
    def collect_providers(self):
        """

        """
        pass

    def get_provider_type(self):
        return self.provider_type
