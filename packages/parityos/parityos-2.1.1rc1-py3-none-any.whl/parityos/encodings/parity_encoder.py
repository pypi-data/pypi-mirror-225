"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Extensions to process the results from the ParityOS cloud services.
"""
from abc import ABC
from typing import Dict

from parityos.base import Qubit


class ParityEncoderExtension(ABC):
    """
    An extends the ParityOSOutput class with the `encode` method.
    This method can transform a bitstring given in the logical system to the parity encoding
    (i.e. to the physical system).
    """

    def encode(self, configuration: Dict[Qubit, int]) -> Dict[Qubit, int]:
        """
        Converts a given configuration in the logical system to a bitstring for the physical mapping

        :param configuration: A logical configuration to encode, the keys are qubits
                              on the physical device, the values are either +1 or -1.
        :return: The configuration in the physical system.
        """
        physical_configuration = {}
        for physical_qubit, parity_map in self.mappings.encoding_map.items():
            # The physical value is the parity of the encoding, times the product of all
            # the values of the physical qubits that encode this logical qubits.
            physical_value = parity_map.parity
            for logical_qubit in parity_map.qubits:
                physical_value *= configuration[logical_qubit]

            physical_configuration[physical_qubit] = physical_value

        return physical_configuration
