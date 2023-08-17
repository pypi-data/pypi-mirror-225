"""
    QuaO Project device_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..enum.provider_type import ProviderType
from ..model.device.aws_braket_device import AwsBraketDevice
from ..model.device.ibm_cloud_device import IbmCloudDevice
from ..model.device.ibm_quantum_device import IbmQuantumDevice
from ..model.device.quao_device import QuaoDevice
from ..model.provider.provider import Provider


class DeviceFactory:
    @staticmethod
    def create_device(provider: Provider,
                      device_specification: str,
                      authentication: dict,
                      sdk: str):
        """
        @param sdk:
        @param provider:
        @param device_specification:
        @param authentication:
        @return:
        """

        provider_type = provider.get_provider_type().value

        if ProviderType.QUAO_QUANTUM_SIMULATOR.value.__eq__(provider_type):
            return QuaoDevice(provider,
                              device_specification,
                              sdk)

        if ProviderType.IBM_QUANTUM.value.__eq__(provider_type):
            return IbmQuantumDevice(provider, device_specification)

        if ProviderType.IBM_CLOUD.value.__eq__(provider_type):
            return IbmCloudDevice(provider, device_specification)

        if ProviderType.AWS_BRAKET.value.__eq__(provider_type):
            return AwsBraketDevice(provider,
                                   device_specification,
                                   authentication.get('bucketName'),
                                   authentication.get('prefix'))

        raise Exception("Unsupported device!")
