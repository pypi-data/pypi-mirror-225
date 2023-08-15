# Copyright 2023 Agnostiq Inc.

from typing import Optional, Dict
from pydantic import BaseModel
from .base import CloudQExecutor


class Options(BaseModel):
    """
    Options for the QiskitExecutor
    """

    optimization_level: int = 3
    resilience_level: int = 3
    max_execution_time: Optional[int] = None
    transpilation: Optional[Dict] = None
    resilience: Optional[Dict] = None
    execution: Optional[Dict] = None
    environment: Optional[Dict] = None
    simulator: Optional[Dict] = None


class QiskitExecutor(CloudQExecutor):
    """
    QiskitExecutor represents the configuration to use when executing the QElectron
    on the Qiskit backend.
    """

    name: str = "qiskit"
    backend: str
    shots: Optional[int] = -1 # -1 means use the `shots` value provided in the QNode's device
    single_job: bool = False
    max_execution_time: int = None
    options: Options = None

    def validate_attrs(self):
        """
        Validate the attributes of the executor and whether they are compatible with the QNode's device.
        Currently validates the `shots` attribute.
        """
        if self.shots <= 0:
            raise ValueError(f"QiskitExecutor does not support setting shots <= 0 current value is {self.shots}. Please check the QNode's device or QiskitExecutor's shot.")
