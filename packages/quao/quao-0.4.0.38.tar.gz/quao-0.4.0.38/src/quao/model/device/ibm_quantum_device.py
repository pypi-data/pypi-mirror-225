"""
    QuaO Project ibm_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from qiskit import transpile

from ...data.device.circuit_running_option import CircuitRunningOption
from ...model.device.qiskit_device import QiskitDevice
from ...config.logging_config import logger


class IbmQuantumDevice(QiskitDevice):

    def _is_simulator(self) -> bool:
        return self.device.configuration().simulator

    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug('Create Ibm Quantum job with {0} shots'.format(options.shots))
        transpile_circuit = transpile(circuit, self.device)

        return self.device.run(transpile_circuit, shots=options.shots)
