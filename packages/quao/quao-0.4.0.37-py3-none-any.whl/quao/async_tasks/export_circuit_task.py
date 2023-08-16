"""
    QuaO Project export_circuit.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

import io

import requests
from braket.circuits import Circuit
from qbraid import circuit_wrapper
from qiskit import transpile, Aer

from ..config.logging_config import logger
from ..enum.media_type import MediaType
from ..enum.provider_type import ProviderType
from ..enum.sdk import Sdk
from ..factory.provider_factory import ProviderFactory
from ..util.http_utils import HttpUtils


def export_circuit_task(
        circuit_config_map: dict,
        backend_config_map: dict,
        user_token: str):
    """
      Export circuit to svg file then send to QuaO server for saving
      Args:
          circuit: circuit will be exported
          @param circuit_config_map: Circuit config map
          @param backend_config_map: Backend config map
          @param user_token: User token
    """

    circuit_export_url = circuit_config_map.get('circuit_export_url')
    if circuit_export_url is None or len(circuit_export_url) < 1:
        return

    logger.debug("Preparing circuit figure...")
    transpiled_circuit = transpile_circuit(circuit_config_map.get('circuit'), backend_config_map)
    circuit_figure = transpiled_circuit.draw(output='mpl', fold=-1)

    logger.debug("Converting circuit figure to svg file...")
    figure_buffer = io.BytesIO()
    circuit_figure.savefig(figure_buffer, format='svg', bbox_inches='tight')

    logger.debug("Sending circuit svg image to [{0}] with POST method ...".format(
        circuit_export_url))

    payload = {'circuit': (
        'circuit_figure',
        figure_buffer.getvalue(),
        MediaType.MULTIPART_FORM_DATA.value)}

    response = requests.post(url=circuit_export_url,
                             headers=HttpUtils.create_bearer_header(user_token),
                             files=payload)

    if response.ok:
        logger.debug("Sending request to QuaO backend successfully!")
    else:
        logger.debug("Sending request to QuaO backend failed with status {0}!".format(
            response.status_code))


def transpile_circuit(circuit, backend_config_map: dict):
    """

    @param circuit: Circuit will be transpiled
    @param backend_config_map: Backend config map
    @return: Transpiled circuit
    """

    if isinstance(circuit, Circuit):
        return circuit_wrapper(circuit).transpile(Sdk.QISKIT.value)

    provider_type = backend_config_map.get('provider_tag')

    if not ProviderType.QUAO_QUANTUM_SIMULATOR.value.__eq__(provider_type):
        provider_type = ProviderType.IBM_QUANTUM.value

    provider = ProviderFactory.create_provider(
        provider_type=provider_type,
        authentication=backend_config_map.get('authentication'))

    backend = provider.get_backend(backend_config_map.get('device_name'))

    return transpile(circuits=circuit, backend=backend)
