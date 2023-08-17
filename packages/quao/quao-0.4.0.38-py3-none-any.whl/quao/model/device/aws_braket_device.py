"""
    QuaO Project aws_braket_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..device.device import Device
from ..provider.provider import Provider
from ...data.device.circuit_running_option import CircuitRunningOption
from ...enum.status.job_status import JobStatus
from ...config.logging_config import logger
from dateutil.parser import parse


class AwsBraketDevice(Device):
    def _get_name(self) -> str:
        return str(self.device.name)

    def __init__(self, provider: Provider,
                 device_specification: str,
                 s3_bucket_name: str,
                 s3_prefix: str):
        super().__init__(provider, device_specification)
        self.s3_folder = (s3_bucket_name, s3_prefix)

    def _create_job(self, circuit,  options: CircuitRunningOption):
        logger.debug('Create AWS Braket job with {0} shots'.format(options.shots))

        job = self.device.run(task_specification=circuit,
                              s3_destination_folder=self.s3_folder,
                              shots=options.shots)
        return job

    def _is_simulator(self) -> bool:
        return 'SIMULATOR'.__eq__(self.device.type.value)

    def _produce_histogram_data(self, job_result) -> dict:
        return dict(job_result.measurement_counts)

    def _get_provider_job_id(self, job) -> str:
        return job.id

    def _get_job_status(self, job) -> str:
        job_state = job.state()
        if JobStatus.COMPLETED.value.__eq__(job_state):
            job_state = JobStatus.DONE.value
        return job_state

    def _calculate_execution_time(self, job_result):
        if 'task_metadata' not in job_result:
            return

        task_metadata = job_result['task_metadata']

        if task_metadata is None \
                or not bool(task_metadata)\
                or 'createdAt' not in task_metadata \
                or 'endedAt' not in task_metadata:
            return

        created_at = task_metadata['createdAt']
        ended_at = task_metadata['endedAt']

        if created_at is None or ended_at is None:
            return

        created_at = parse(created_at.replace("T", " ").replace("Z", ""))
        ended_at = parse(ended_at.replace("T", " ").replace("Z", ""))

        offset = ended_at - created_at

        self.execution_time = offset.total_seconds()
