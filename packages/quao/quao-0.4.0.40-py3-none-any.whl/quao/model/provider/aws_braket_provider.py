"""
    QuaO Project aws_braket_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import boto3
from braket.aws import AwsSession, AwsDevice

from ...enum.provider_type import ProviderType
from ...model.provider.provider import Provider
from ...config.logging_config import *


class AwsBraketProvider(Provider):

    def __init__(self, aws_access_key, aws_secret_access_key, region_name):
        super().__init__(ProviderType.AWS_BRAKET)
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name

    def get_backend(self, device_specification: str):
        """

        @param device_specification:
        """

        session = self.collect_providers()
        return AwsDevice(
            arn=device_specification,
            aws_session=session)

    def collect_providers(self):
        """

        """

        logger.debug('Connect to Aws Braket provider')
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name)

        return AwsSession(boto_session=session)
