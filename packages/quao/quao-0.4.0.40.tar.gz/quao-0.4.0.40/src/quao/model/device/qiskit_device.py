"""
    QuaO Project qiskit_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import ABC

from qiskit import QiskitError

from ...model.device.device import Device
from ...config.logging_config import logger


class QiskitDevice(Device, ABC):

    def _produce_histogram_data(self, job_result) -> dict:
        try:
            histogram_data = job_result.get_counts()
        except QiskitError as qiskit_error:
            logger.debug("Can't produce histogram with error: {0}".format(str(qiskit_error)))
            histogram_data = None

        return histogram_data

    def _get_provider_job_id(self, job) -> str:
        return job.job_id()

    def _get_job_status(self, job) -> str:
        return job.status().name

    def _get_name(self) -> str:
        return str(self.device.configuration().backend_name)

    def _calculate_execution_time(self, job_result):
        if "metadata" not in job_result:
            return None

        metadata = job_result["metadata"]

        if metadata is None or not bool(metadata) or "time_taken_execute" not in metadata:
            return None

        self.execution_time = metadata["time_taken_execute"]
