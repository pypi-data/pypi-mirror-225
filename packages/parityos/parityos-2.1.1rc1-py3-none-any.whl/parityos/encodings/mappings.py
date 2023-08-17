"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Tools to connect to the ParityOS cloud services and to process the results.
"""
from dataclasses import dataclass
from typing import FrozenSet, List, Mapping

from parityos.base import Qubit, EqualityConstraint, json_wrap, JSONMappingType


@dataclass(frozen=True)
class ParityMap:
    """
    A class that represents a set of qubits and a parity value,
    to facilitate serialization of Mappings.
    """

    qubits: FrozenSet[Qubit]
    parity: int

    @classmethod
    def from_json(cls, data):
        """
        Initializes a ParityMap object from json

        :param data: parity map in json format
        :return: A ParityMap instance
        """
        qubits_data, parity = data
        qubits = frozenset(Qubit(label) for label in qubits_data)
        return cls(qubits, parity)

    def to_json(self):
        """
        Converts a Parity Map object to json

        :return: the parity map in json format
        """
        return json_wrap([self.qubits, self.parity])


@dataclass(frozen=True)
class Mappings:
    """
    Holds the Parity Architecture encoding and decoding maps returned from the API.

    :param logical_degeneracies: the list of how logical degeneracies are fixed
    :param encoding_map: the encoding map, which tells you how to go from each physical qubit
                         to the logical qubits that it encodes.
    :param decoding_map: A possible decoding map, which tells you how to go from a logical
                         qubit to a list of physical qubits that multiply to the logical
                         qubit.
    """

    logical_degeneracies: List[ParityMap]
    encoding_map: Mapping[Qubit, ParityMap]
    decoding_map: Mapping[Qubit, ParityMap]

    def to_json(self):
        """
        Converts a Mappings object to json

        :return: the mappings in json format
        """
        return json_wrap(
            {
                "logical_degeneracies": self.logical_degeneracies,
                "encoding_map": self.encoding_map.items(),
                "decoding_map": self.decoding_map.items(),
            }
        )

    @classmethod
    def from_json(cls, data: JSONMappingType):
        """
        Constructs a Mappings object from json data

        :param data: the mappings in json format
        :return: a Mappings object
        """

        logical_degeneracies = [
            ParityMap.from_json(parity_map_data) for parity_map_data in data["logical_degeneracies"]
        ]
        encoding_map = {
            Qubit(coordinate): ParityMap.from_json(parity_map_data)
            for coordinate, parity_map_data in data["encoding_map"]
        }
        # This only works if the original qubit labels were numbers or strings
        decoding_map = {
            Qubit(qubit): ParityMap.from_json(parity_map_data)
            for qubit, parity_map_data in data["decoding_map"]
        }
        return cls(logical_degeneracies, encoding_map, decoding_map)
