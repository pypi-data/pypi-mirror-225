"""
ParityQC GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Equality constraints that form part of compiled problems
or that define additional logical side conditions.
"""
from typing import Iterable
from warnings import warn

from parityos.base.qubits import Qubit
from parityos.base.utils import json_wrap


class EqualityConstraint:
    """
    Represents an equality constraint of the form:
    :math:`s_1 \\cdot s_2 \\dots \\cdot s_n = \\pm 1`,
    where :math:`s_1 \\dots s_n` are spin variables.
    """

    def __init__(self, operator: Iterable[Qubit], value: int):
        """
        :param operator: The operator that defines the constraint.
                         Given as a collection of qubits, the operator is then the product
                         of Z operators on each of the qubits.
        :param value: parity of the constraint; must be +1 or -1.
        """
        try:
            assert abs(value) == 1  # This test also works for float and numpy types.
        except AssertionError:
            raise ValueError("The value of an equality constraint must be either 1 or -1.")

        self.qubits = frozenset(operator)
        self.value = int(value)

    @classmethod
    def from_json(cls, constraint_data):
        """
        Initializes an EqualityConstraint object from json

        :param constraint_data: The constraint in json format.
        :return: An EqualityConstraint instance.
        """
        qubits_data, value = constraint_data
        qubits = frozenset(Qubit(label) for label in qubits_data)
        return cls(qubits, value)

    def to_json(self):
        """
        Converts the EqualityConstraint object to json

        :return: The constraint in json format.
        """
        return json_wrap([self.qubits, self.value])

    def __eq__(self, other):
        return (self.value == other.value) and (self.qubits == other.qubits)

    def __repr__(self):
        return f"{self.__class__.__name__}({set(self.qubits)}, {self.value})"

    def __hash__(self):
        return hash((type(self), self.qubits, self.value))


class ParityConstraint(EqualityConstraint):
    """The deprecated version of the EqualityConstraint class

    Represents a parity constraint, which means a condition of the form:
    :math:`s_1 \\cdot s_2 \\dots \\cdot s_n = \\pm 1` (where `s_1 \\dots s_n` are spin variables).

    :param qubits: a collection of qubits that make up this constraint
    :param parity: parity of the constraint; must be +1 or -1.
    """

    def __init__(self, qubits: Iterable[Qubit], parity: int):
        warn(
            "The ParityConstraint class is deprecated. "
            "Please use the EqualityConstraint class instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        # stack level 2 raises the warning at the level of the caller,
        # instead of the level of this __init__ method
        super().__init__(qubits, value=parity)
