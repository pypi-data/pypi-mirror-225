"""
    QuaO Project ibm_cloud_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import QiskitRuntimeService

from ...enum.provider_type import ProviderType
from ...model.provider.provider import Provider
from ...config.logging_config import *


class IbmCloudProvider(Provider):

    def __init__(self, api_key, crn):
        super().__init__(ProviderType.IBM_CLOUD)
        self.api_key = api_key
        self.crn = crn
        self.channel = 'ibm_cloud'

    def get_backend(self, device_specification: str):
        """

        @param device_specification:
        @return:
        """
        provider = self.collect_providers()

        return provider.get_backend(name=device_specification)

    def collect_providers(self):
        """

        @return:
        """

        logger.debug('Connect to Ibm Cloud provider')
        return QiskitRuntimeService(channel=self.channel, token=self.api_key, instance=self.crn)
