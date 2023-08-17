"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Classes that store information on sequences of quantum gates
"""
from math import pi
from typing import Iterator, Mapping, Set, Union

from parityos.base.qubits import Qubit
from parityos.base.gates import Gate, CNOT, Rx, Ry, Rz, Rzz
from parityos.base.utils import json_wrap, JSONLoadSaveMixin
from parityos.base.exceptions import ParityOSException


class Circuit(JSONLoadSaveMixin, list):
    """
    A sequence of Gate and/or Circuit objects.
    """

    @property
    def qubits(self) -> Set[Qubit]:
        """
        :return: All qubits from the elements in the circuit
        """
        return set().union(*(element.qubits for element in self))

    @classmethod
    def from_json(cls, data):
        """
        Creates a Circuit from a list of elements in json

        :param data: a list of elements in json format
        :return: a Circuit object
        """
        data = _remove_empty_lists(data)
        args = (
            Gate.from_json(element_data)
            if isinstance(element_data[0], str)
            else cls.from_json(element_data)
            for element_data in data
        )
        return cls(args)

    def to_json(self):
        """
        Converts the Container to json

        :return: a list with the elements of the circuit in json format
        """
        return [json_wrap(element) for element in self]

    def remap(self, context: Mapping = None, **kwargs) -> "Circuit":
        """
        Creates a copy of the circuit where the remap has been applied to all parametrized gates
        in the circuit (see `gates.RMixin.remap` for details).

        :param context: a mapping of parameter names (strings) to parameter values (number-like
                        objects) or to new parameter names (strings).
        """
        return Circuit((element.remap(context=context, **kwargs) for element in self))

    def __repr__(self):
        args = ", ".join(repr(element) for element in self)
        return f"{self.__class__.__name__}([{args}])"


CircuitElement = Union[Gate, Circuit]
HALF_PI = 0.5 * pi


def convert_cnots_to_rzzs(circuit: Circuit) -> Circuit:
    """
    ZZ rotations instead of CNOTs.

    Replaces the standards CNOTs on the optimized circuit with an equivalent implementation based on
    ZZ and local rotations. The resulting circuit will contain additional subcircuits to account
    for the necessary Rx, Ry and Rz rotations.

    :param circuit: a circuit containing moments with CNOT gates.
    :type circuit: Circuit
    :return: a new circuit where all CNOTs have been replaced by ZZ and local rotations.
    :rtype: Circuit
    """
    new_circuit = Circuit()
    for subcircuit in circuit:
        if not isinstance(subcircuit, Circuit):
            # This situation can occur when gates and subcircuits were mixed together at the same
            # level. We raise an error in this case, because this method expects gates to be grouped
            # in moments (i.e. parallelizable subcircuits).
            raise ParityOSException(
                "Unexpected mix of gates and subcircuits encountered. Please "
                "organize gates in moments (parallelizable subcircuits)."
            )
        elif all(isinstance(element, Gate) for element in subcircuit):
            new_circuit.extend(_convert_moment(subcircuit))
        else:
            new_circuit.append(convert_cnots_to_rzzs(subcircuit))

    return new_circuit


def _convert_moment(circuit) -> Iterator[Circuit]:
    """
    A helper function for convert_cnots_to_rzzs.
    Lowest level circuits are expanded and have cnots turned into rzzs. This results in additional
    circuits to be added before and after the moment circuit to account for the necessary Rx, Ry
    and Rz rotations.

    :return: a list of circuits representing the original circuit where cnots have been converted to
        rzz gates.
    """
    before, moment, after1, after2 = Circuit(), Circuit(), Circuit(), Circuit()
    # Representing a Cnot as a ZZ interaction requires the injection of a moment before and two
    # moments after the original moment.
    for gate in circuit:
        if not isinstance(gate, CNOT):
            # Copy the other gates directly to the new moment.
            moment.append(gate)
        else:
            control, target = gate.qubit_list
            # Add the necessary rotation before the ZZ interaction.
            before.append(Ry(target, -HALF_PI))
            # Replace the CNOT with a ZZ rotation.
            moment.append(Rzz(control, target, -HALF_PI))
            # Add the remaining rotations after the ZZ interaction.
            after1.append(Rx(target, HALF_PI))
            after2.append(Rz(control, HALF_PI))
            after2.append(Rz(target, HALF_PI))

    return (subcircuit for subcircuit in [before, moment, after1, after2] if subcircuit)


def _remove_empty_lists(data):
    empty_list = []
    for _ in range(data.count(empty_list)):
        data.remove(empty_list)
    return data
