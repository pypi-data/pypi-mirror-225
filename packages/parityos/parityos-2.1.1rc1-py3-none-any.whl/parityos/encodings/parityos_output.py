"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Container class for the results from the ParityOS compiler.
"""

from parityos.base import json_wrap, dict_filter, JSONLoadSaveMixin, ProblemRepresentation, Rz
from parityos.base.circuit import Circuit, convert_cnots_to_rzzs
from parityos.encodings.mappings import Mappings
from parityos.encodings.parity_decoder import ParityDecoderExtension
from parityos.encodings.parity_encoder import ParityEncoderExtension


class ParityOSOutput(JSONLoadSaveMixin, ParityEncoderExtension, ParityDecoderExtension):
    def __init__(
        self,
        compiled_problem: ProblemRepresentation,
        mappings: Mappings,
        constraint_circuit: Circuit = None,
        problem_circuit: Circuit = None,
        driver_circuit: Circuit = None,
        initial_state_preparation_circuit: Circuit = None,
    ):
        r"""
        This class contains all the output that ParityOS produces, this may be extended
        with extra features in the future, but for now it contains the compiled problem,
        the mappings and in case of digital devices also the constraint circuit.

        :param compiled_problem: compiled problem representation with parity constraints
        :param mappings: Mappings object representing the mapping between the logical
                         and the physical problem.
        :param constraint_circuit: constraint Circuit (:math:`e^{-i \theta Z_1 Z_2 Z_3 [Z_4] /2}` )
                                   for digital devices or None for analog devices.
        :param problem_circuit: problem circuit implementing the spin Hamiltonian corresponding to
                                the logical problem for digital devices or None for analog devices.
        :param driver_circuit: optional driver Circuit for digital devices
                               or None for analog devices.
        :param initial_state_preparation_circuit: The initial-state preparation circuit tells
            how to make the initial state, starting from the computational basis state
            :math:`|0\langle^K`. For normal QAOA, one would want to start in the
            :math:`|+\langle^K` state for all qubits, so it would be a combination of RX and RZ
            or a Hadamard. The gates in this circuit are fixed,
            as they do not have a QAOA parameter, but should be executed with this exact angle.
        """
        self.compiled_problem = compiled_problem
        self.mappings = mappings
        self.constraint_circuit = constraint_circuit
        self.problem_circuit = problem_circuit or self.create_default_problem_circuit()
        self.driver_circuit = driver_circuit
        self.initial_state_preparation_circuit = initial_state_preparation_circuit

    @property
    def logical_problem_circuit(self) -> Circuit:
        """
        The same as self.problem_circuit, for compatibility.
        """
        return self.problem_circuit

    def create_default_problem_circuit(self) -> Circuit:
        """
        Create a circuit that implements $ \\exp(i \\mbox{parameter} H) $, where H is the
        spin Hamiltonian of the compiled problem representation. This spin Hamiltonian encodes
        the spin interactions of the original problem representation. Equality conditions from
        the original problem representation will have been absorbed in the parity constraints,
        for which the `constraint_circuit` attribute provides a separate circuit.

        :return: a Circuit instance that implements the exponential of the Hamiltonian.
        """
        moment = Circuit()
        for interaction, strength in self.compiled_problem.terms:
            if len(interaction) == 1:
                [qubit] = interaction  # Grab the first and only element from the interaction
                moment.append(Rz(qubit, strength, parameter_name="parameter"))
            else:
                missing_gate = f"R{'z' * len(interaction)}"
                raise NotImplementedError(f"{missing_gate} gate not available")

        return Circuit([moment])

    def replace_cnots_by_rzzs(self):
        """
        Replace the CNOT gates in self.constraint_circuit by ZZ and local rotations.
        This is useful for devices that have native ZZ rotations instead of native CNOTs.
        It replaces the self.constraint_circuit attribute in place.
        """
        self.constraint_circuit = convert_cnots_to_rzzs(self.constraint_circuit)

    @classmethod
    def from_json(cls, data: dict) -> "ParityOSOutput":
        """
        Creates the ParityOSOutput class from the format in the response schema.

        :param data: a JSON-like dictionary as specified in the response schema.
        :return: a ParityOSOutput object
        """
        # We reorganize the JSON data to match the definitions of CompiledProblem:
        # the 'hamiltonian' field in 'compiled_problem' is flattened.
        # Once the JSON schema has been updated in the API, these lines can be removed.
        compiled_problem_data = data["compiled_problem"]
        if "hamiltonian" in compiled_problem_data:
            compiled_problem_data = {
                **compiled_problem_data["hamiltonian"],
                **dict_filter(compiled_problem_data, {"constraints"}),
            }

        kwargs = {
            "compiled_problem": ProblemRepresentation.from_json(compiled_problem_data),
            "mappings": Mappings.from_json(data["mappings"]),
        }
        optimization_data = data.get("optimization", {})
        for key in {
            "constraint_circuit",
            "problem_circuit",
            "driver_circuit",
            "initial_state_preparation_circuit",
        }:
            circuit_data = optimization_data.get(key)
            if circuit_data:
                kwargs[key] = Circuit.from_json(circuit_data)

        return cls(**kwargs)

    def to_json(self):
        """
        Repackages self into the response schema dictionary.

        :return: dictionary as specified in the response schema
        """
        data_map = {
            "compiled_problem": self.compiled_problem,
            "mappings": self.mappings,
        }
        optimization = {
            "constraint_circuit": self.constraint_circuit,
            "problem_circuit": self.problem_circuit,
            "driver_circuit": self.driver_circuit,
            "initial_state_preparation_circuit": self.initial_state_preparation_circuit,
        }
        optimization = {key: value for key, value in optimization.items() if value}
        if optimization:
            data_map["optimization"] = optimization

        return json_wrap(data_map)

    def __repr__(self):
        args = (
            self.compiled_problem,
            self.mappings,
            self.constraint_circuit,
            self.problem_circuit,
            self.driver_circuit,
            self.initial_state_preparation_circuit,
        )
        return f"{self.__class__.__name__}{args}"
