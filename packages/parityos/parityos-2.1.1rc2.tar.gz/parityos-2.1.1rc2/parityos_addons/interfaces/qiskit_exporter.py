"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Tools to export ParityOS circuits to Qiskit.
"""
from typing import Any, Iterable, Mapping, Tuple, Iterator

from parityos.base.circuit import CircuitElement
from parityos.base.gates import Qubit, Gate, RMixin, CNOT, H, X, Y, Z, Rx, Ry, Rz, Rzz
from parityos.base.exceptions import ParityOSImportError

try:
    import qiskit
    import qiskit.circuit.library as qiskit_library
except ImportError:
    raise ParityOSImportError("The Qiskit exporter requires the installation of Qiskit")


GATE_MAP = {
    CNOT: qiskit_library.CXGate,
    H: qiskit_library.HGate,
    X: qiskit_library.XGate,
    Y: qiskit_library.YGate,
    Z: qiskit_library.ZGate,
    Rx: qiskit_library.RXGate,
    Ry: qiskit_library.RYGate,
    Rz: qiskit_library.RZGate,
    Rzz: qiskit_library.RZZGate,
}


class QiskitExporter:
    """
    Tool to convert ParityOS circuits to Qiskit quantum circuits.

    Instantiate the QiskitExporter with a qubit map and a parameter map.
    Then use the `to_qiskit` method to convert a ParityOS circuit to Qiskit quantum circuit.

    EXAMPLE:
        from qiskit.circuit import Parameter
        parameter_map = {'theta': Parameter('$\\theta$'), 'gamma': Parameter('$\\gamma$')}
        qiskit_exporter = QiskitExporter(parameter_map)
        qiskit_circuit = qiskit_exporter.to_qiskit(parityos_circuit)
    """

    def __init__(
        self,
        parameter_map: Mapping[str, Any] = None,
        qubit_map: Mapping[Qubit, int] = None,
        qubits: Iterable[Qubit] = None,
    ):
        """
        Converts the circuit to a Qiskit circuit.

        :param parameter_map: a mapping of the form {parameter_name: parameter_value}, where the
            parameter_name is a string that is used as a parameter_name in the ParityOS circuit,
            and parameter_value is a number like object (int, float, numpy float or a Qiskit
            Parameter object are all valid). Optional. If not given, then an empty dictionary is
            used instead.
        :param qubit_map: a mapping of the form {ParityOS_qubit: qubit_index}, where qubit_index is
            the integer index of the qubit in the Qiskit qubit register. Optional.
        :param qubits: an iterable of ParityOS qubits. This is used to generate a qubit_map where
            each qubit is mapped onto its index in the sequence. Optional.
            Either a `qubit_map` or a `qubits` iterable must be given.

        """
        self.parameter_map = {} if parameter_map is None else parameter_map
        if qubit_map:
            self.qubit_map = qubit_map
        elif qubits:
            self.qubit_map = {qubit: i for i, qubit in enumerate(qubits)}
        else:
            raise TypeError("QiskitExporter requires either a qubit_map or qubits argument")

    def to_qiskit(self, circuit: CircuitElement) -> qiskit.QuantumCircuit:
        """
        Converts the circuit to a Qiskit quantum circuit.

        :param circuit: a ParityOS circuit of quantum gates.
        :return: a Qiskit QuantumCircuit object.
        """
        qiskit_circuit = qiskit.QuantumCircuit(len(self.qubit_map))

        def _qiskit_circuit_append(element: CircuitElement):
            """Recursive helper method for the to_qiskit method."""
            if isinstance(element, Gate):
                qiskit_circuit.append(*self.gate_to_qiskit(element))
            else:
                for item in element:
                    _qiskit_circuit_append(item)

        _qiskit_circuit_append(circuit)
        return qiskit_circuit

    def gate_to_qiskit(self, gate) -> Tuple[qiskit.circuit.gate.Gate, Iterator[int]]:
        """
        Converts a gate to a (Qiskit instruction, qubit_indices) tuple.

        :param gate: a ParityOS gate instance.
        :return: a (Qiskit instruction, qubit_indices) tuple.
        """
        qiskit_class = GATE_MAP[type(gate)]
        if isinstance(gate, RMixin):
            angle = (
                gate.angle
                if gate.parameter_name is None
                else gate.angle * self.parameter_map[gate.parameter_name]
            )
            qiskit_instruction = qiskit_class(angle)
        else:
            qiskit_instruction = qiskit_class()

        qubit_indices = (
            self.qubit_map[qubit] for qubit in gate.make_args() if isinstance(qubit, Qubit)
        )
        return qiskit_instruction, qubit_indices
