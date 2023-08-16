"""
    QuaO Project provider_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..enum.provider_type import ProviderType
from ..model.provider.aws_braket_provider import AwsBraketProvider
from ..model.provider.ibm_cloud_provider import IbmCloudProvider
from ..model.provider.ibm_quantum_provider import IbmQuantumProvider
from ..model.provider.quao_provider import QuaoProvider


class ProviderFactory:
    @staticmethod
    def create_provider(provider_type: str, authentication: dict):
        """

        @param provider_type:
        @param authentication:
        @return:
        """

        if ProviderType.QUAO_QUANTUM_SIMULATOR.value.__eq__(provider_type):
            return QuaoProvider()

        if ProviderType.IBM_QUANTUM.value.__eq__(provider_type):
            return IbmQuantumProvider(authentication.get("token"))

        if ProviderType.IBM_CLOUD.value.__eq__(provider_type):
            return IbmCloudProvider(
                authentication.get("token"), authentication.get("crn")
            )

        if ProviderType.AWS_BRAKET.value.__eq__(provider_type):
            return AwsBraketProvider(
                authentication.get("accessKey"),
                authentication.get("secretKey"),
                authentication.get("regionName"),
            )

        raise Exception("Unsupported provider!")
