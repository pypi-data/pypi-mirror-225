"""
    QuaO Project quao_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import transpile
from qiskit import QiskitError

from ...data.device.circuit_running_option import CircuitRunningOption
from ...enum.status.job_status import JobStatus
from ...enum.processing_unit import ProcessingUnit
from ...enum.sdk import Sdk
from ..device.device import Device
from ..provider.provider import Provider
from ...config.logging_config import logger


class QuaoDevice(Device):

    def __init__(self, provider: Provider,
                 device_specification: str,
                 sdk: str):
        super().__init__(provider, device_specification)
        self.sdk = sdk

    def _get_name(self) -> str:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return str(self.device.configuration().backend_name)

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return str(self.device.name)

        raise Exception("Sdk not supported!")

    def _create_job(self, circuit,  options: CircuitRunningOption):
        logger.debug('Create Quao job with {0} shots'.format(options.shots))
        if Sdk.QISKIT.value.__eq__(self.sdk):
            self.device.set_options(device=options.processing_unit.value,
                                    shots=options.shots,
                                    executor=options.executor,
                                    max_job_size=options.max_job_size)
            transpiled_circuit = transpile(circuits=circuit, backend=self.device)

            return self.device.run(transpiled_circuit)

        if Sdk.BRAKET.value.__eq__(self.sdk):
            import time

            start_time = time.time()

            job = self.device.run(task_specification=circuit, shots=options.shots)

            self.execution_time = time.time() - start_time

            return job

        raise Exception("Sdk not supported!")

    def _is_simulator(self) -> bool:
        return True

    def _produce_histogram_data(self, job_result) -> dict:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            try:
                histogram_data = job_result.get_counts()
            except QiskitError as qiskit_error:
                logger.debug("Can't produce histogram with error: {0}".format(str(qiskit_error)))
                histogram_data = None

            return histogram_data

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return dict(job_result.measurement_counts)

    def _get_provider_job_id(self, job) -> str:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return job.job_id()

        if Sdk.BRAKET.value.__eq__(self.sdk):
            return job.id

    def _get_job_status(self, job) -> str:
        if Sdk.QISKIT.value.__eq__(self.sdk):
            return job.status().name

        if Sdk.BRAKET.value.__eq__(self.sdk):
            job_state = job.state()
            if JobStatus.COMPLETED.value.__eq__(job_state):
                job_state = JobStatus.DONE.value
            return job_state

    def _calculate_execution_time(self, job_result):
        if Sdk.QISKIT.value.__eq__(self.sdk):
            if "metadata" not in job_result:
                return None
    
            metadata = job_result["metadata"]
    
            if (
                metadata is None
                or not bool(metadata)
                or "time_taken_execute" not in metadata
            ):
                return None
    
            self.execution_time = metadata["time_taken_execute"]
