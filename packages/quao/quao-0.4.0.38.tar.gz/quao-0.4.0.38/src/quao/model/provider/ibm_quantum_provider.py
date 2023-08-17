"""
    QuaO Project ibm_quantum_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_provider import IBMProvider

from ...enum.provider_type import ProviderType
from ...model.provider.provider import Provider
from ...config.logging_config import *


class IbmQuantumProvider(Provider):
    def __init__(self, api_token):
        super().__init__(ProviderType.IBM_QUANTUM)
        self.api_token = api_token

    def get_backend(self, device_specification: str):
        """

        @param device_specification:
        """

        provider = self.collect_providers()

        return provider.get_backend(device_specification)

    def collect_providers(self):
        """

        @return:
        """

        logger.debug('Connect to Ibm Quantum provider')
        return IBMProvider(token=self.api_token)
