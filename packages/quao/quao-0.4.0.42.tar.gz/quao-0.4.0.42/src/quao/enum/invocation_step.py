from enum import Enum


class InvocationStep(Enum):
    POLLING = "POLLING"
    PREPARATION = "PREPARATION"
    EXECUTION = "EXECUTION"
    ANALYSIS = "ANALYSIS"
    FINALIZATION = "FINALIZATION"
    PROMISE = "PROMISE"
