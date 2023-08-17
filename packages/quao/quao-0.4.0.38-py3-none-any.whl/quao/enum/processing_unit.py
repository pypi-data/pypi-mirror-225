"""
    QuaO Project processing_unit.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from enum import Enum


class ProcessingUnit(Enum):
    CPU = 'CPU'
    GPU = 'GPU'
    QPU = 'QPU'
