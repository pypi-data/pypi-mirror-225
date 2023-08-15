"""
    QuaO Project ibm_cloud_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit_ibm_runtime import Options, Session, Sampler

from ...data.device.circuit_running_option import CircuitRunningOption
from ...model.device.qiskit_device import QiskitDevice
from ...config.logging_config import *


class IbmCloudDevice(QiskitDevice):
    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _create_job(self, circuit,  options: CircuitRunningOption):
        logger.debug('Create Ibm Cloud job with {0} shots'.format(options.shots))
        running_options = Options(optimization_level=1)
        running_options.execution.shots = options.shots

        with Session(service=self.provider.collect_providers(), backend=self.device) as session:
            sampler = Sampler(session=session, options=running_options)
            job = sampler.run(circuits=circuit)

            return job
