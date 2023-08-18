"""
    QuaO Project quao_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_aer import Aer

from ...enum.provider_type import ProviderType
from ...model.provider.provider import Provider
from braket.devices import LocalSimulator
from ...config.logging_config import *


class QuaoProvider(Provider):
    def __init__(self):
        super().__init__(ProviderType.QUAO_QUANTUM_SIMULATOR)

    def get_backend(self, device_specification):
        """

        @param device_specification:
        @return:
        """

        providers = self.collect_providers()

        aer_device_names = set(map(self.__map_aer_backend_name, providers[0].backends()))
        aws_device_names = providers[1].registered_backends()

        if aer_device_names.__contains__(device_specification):
            backend = providers[0].get_backend(device_specification)

            return backend

        if aws_device_names.__contains__(device_specification):
            return LocalSimulator(device_specification)

        raise Exception('Unsupported device')

    def collect_providers(self):
        """

        @return:
        """
        logger.debug('Connect to Quao provider')
        return [Aer, LocalSimulator()]

    @staticmethod
    def __map_aer_backend_name(backend):
        return backend.configuration().backend_name
