"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Classes that store information on quantum gate operations.
"""
from abc import ABC
from typing import Mapping, Set, Tuple

from parityos.base.qubits import Qubit
from parityos.base.utils import json_wrap, JSONType


class Gate(ABC):
    """
    Base class from which all gates inherit.

    The Gate subclasses are intended to store the information received from the compiler.
    They do not implement any methods to simulate the gates, nor do they contain any information
    on the (anti-) commutation relations between them or other mathematical properties.
    For those uses we recommend more elaborate frameworks like Qutip, Cirq or Qiskit.
    """

    _gate_map = {}  # a Dict that maps gate names onto gate classes (used by from_json)
    aliases = tuple()  # Alternative names for the class that could appear in JSON representations.

    def __init__(self, *qubit_args: Qubit):
        """
        Set up the list of qubits on which the gate acts.
        """
        self.qubit_list = list(qubit_args)

    def __init_subclass__(cls):
        """
        Update the gate map when a new subclass is defined.
        This is used by the `from_json` method to map the JSON data on the correct gate class.
        """
        super().__init_subclass__()
        Gate._gate_map[cls.__name__] = cls
        Gate._gate_map.update({alias: cls for alias in cls.aliases})

    @property
    def qubits(self) -> Set[Qubit]:
        """
        :return: the set of qubits on which the gate acts (including possible control qubits).
        """
        return set(self.qubit_list)

    def make_args(self) -> Tuple[Qubit]:
        """
        :return: the sequence of arguments that would be needed to instantiate a copy of self
            (does not include keyword only arguments).
        """
        return tuple(self.qubit_list)

    def to_json(self) -> JSONType:
        """
        :return: a json compatible object with all the information about the gate.
        """
        return json_wrap([type(self).__name__, *self.make_args()])

    @classmethod
    def from_json(cls, data) -> "Gate":
        """
        Creates a gate from a json compatible object.

        :param data: gate parameters in json compatible format
        :return: a Gate instance
        """
        # This method redirects the Gate.from_json method to the cls.from_json method,
        # where cls is taken from Gate._gate_map based on the first value in the data.
        gate_class_name, *gate_data = data
        gate_class = cls._gate_map[gate_class_name]
        if cls is Gate:
            # For the abstract class, we delegate to the concrete class.
            return gate_class.from_json(data)
        elif cls is gate_class:
            # Here we define the standard behavior for concrete subclasses.
            # Subclasses can overwrite this if they need more elaborate gate data processing.
            qubit_args = (Qubit(label) for label in gate_data)
            return cls(*qubit_args)
        else:
            raise ValueError(f"Incorrect gate class for {gate_class_name} gate")

    def remap(self, *args, **kwargs) -> "Gate":
        """
        The `RMixin.remap` method is used to remap the parameter name of parametrized gates to new
        values. For other gates (the subject of this version), a simple copy of the gate is
        returned.
        """
        # *args and **kwargs are listed (but not consumed) to make sure that the signature is
        # compatible with the signature of Rmixin.remap
        return type(self)(*self.make_args())

    def __repr__(self):
        arguments = ", ".join(repr(arg) for arg in self.make_args())
        return f"{type(self).__name__}({arguments})"

    def __eq__(self, other):
        return (type(self) == type(other)) and (self.make_args() == other.make_args())

    def __hash__(self):
        return hash((type(self), self.make_args()))


class Gate1(Gate):
    """
    A Gate that acts on a single qubit.
    """

    def __init__(self, qubit: Qubit):
        """
        :param Qubit qubit: qubit on which the gate acts.
        """
        # We implement __init__ to enforce a single qubit argument
        super().__init__(qubit)


class Gate2(Gate):
    """
    A Gate that acts on two qubits.
    """

    def __init__(self, qubit1: Qubit, qubit2: Qubit):
        """
        :param Qubit qubit1, qubit2: qubits on which the gate acts.
        """
        # We implement __init__ to enforce exactly two qubit arguments
        super().__init__(qubit1, qubit2)


class Gate3(Gate):
    """
    A Gate that acts on three qubits.
    """

    def __init__(self, qubit1: Qubit, qubit2: Qubit, qubit3: Qubit):
        """
        :param Qubit qubit1, qubit2, qubit3: qubits on which the gate acts.
        """
        # We implement __init__ to enforce exactly three qubit arguments
        super().__init__(qubit1, qubit2, qubit3)


class Gate4(Gate):
    """
    A Gate that acts on four qubits.
    """

    def __init__(self, qubit1: Qubit, qubit2: Qubit, qubit3: Qubit, qubit4: Qubit):
        """
        :param Qubit qubit1, qubit2, qubit3, qubit4: qubits on which the gate acts.
        """
        # We implement __init__ to enforce exactly four qubit arguments
        super().__init__(qubit1, qubit2, qubit3, qubit4)


class RMixin:
    """
    A mixin that converts a gate into a rotated gate.

    Attributes:
        angle: the angle for the gate rotation
        parameter_name: a label that identifies the parameter with which to multiply
        the angle when implementing it. If no parameter name is given, then the gate is
        considered to be a 'Fixed' gate. If a parameter name is given, then the gate is
        considered to be a 'Parametrized' gate. This is reflected in the name of the gate
        in the output generated by the `to_json` method.
    """

    _FIXED = "Fixed"
    _PARAMETRIZED = "Parametrized"
    _DEFAULT_PARAMETER_NAME = "parameter"

    def __init_subclass__(cls):
        """
        Update the gate map with the class name + suffixes when a new subclass is defined.
        """
        cls.aliases = f"{cls.__name__}{cls._FIXED}", f"{cls.__name__}{cls._PARAMETRIZED}"
        super().__init_subclass__()

    def __init__(self, *args: Qubit, parameter_name: str = None, **kwargs):
        """
        :param Qubit args: a list of Qubits on which the gate acts
        :param float angle: the angle for the gate rotation
        :param str parameter_name: a label that identifies the parameter with which to multiply
                                   the angle when implementing it.
        """
        # angle is a mandatory argument, but it should be given after the qubit args.
        if "angle" in kwargs:
            super_args = args
            angle = kwargs.pop("angle")
        else:
            *super_args, angle = args

        super().__init__(*super_args, **kwargs)
        self.angle = angle
        self.parameter_name = parameter_name

    def remap(self, context: Mapping = None, **kwargs) -> Gate:
        """
        Creates a copy of the gate with an updated parameter or parameter name.

        Updates for the parameter should be provided either as a context mapping or as a keyword
        argument. If a keyword argument is given, its key must match the parameter_name defined
        on the gate, otherwise an error will be raised.
        If no keyword argument is given, then the parameter_name is looked up in the context. If it
        is found, then the parameter is remapped to the corresponding value. Otherwise, a copy of
        the gate is returned.

        If the provided value is a string, then it is interpreted as a new parameter name and the
        resulting gate is again a parametrized gate.
        Otherwise, the value should be a number-like object (an int, a float, a numpy float or even
        a Sympy symbol or a Qiskit Parameter can be used). Then the returned gate is a fixed gate
        where the angle has been multiplied with the number-like object.

        A keyword argument takes precedence over the context argument.

        :param context: a mapping of parameter names (strings) to parameter values (number-like
                        objects) or to new parameter names (strings).


        Examples:
            rz_gate = RZ(Qubit(1), angle=math.pi, parameter_name='parameter')
            # Create a copy of rz_gate where the parameter_name is changed to 'theta'.
            rz_theta = rz_gate.remap(parameter='theta')
            rz_theta = rz_gate.remap({'parameter': 'theta', 'other_parameter': 'gamma'})

            # Convert rz_theta into a fixed gate with the angle divided by two:
            rz_fixed = rz_theta.remap(theta=0.5)
            rz_fixed = rz_theta.remap({'theta': 0.5, 'gamma': 2.5})
        """
        if context is None:
            context = {}

        if self.parameter_name is None:
            # For a fixed gate, simply return a copy of the original gate.
            return super().remap(context=context, **kwargs)

        value = (
            kwargs[self.parameter_name]
            if kwargs
            else context.get(self.parameter_name, self.parameter_name)
        )
        # The second argument self.parameter_name makes sure that we create a copy of the
        # original gate if self.parameter_name was not included in the context.

        cls = type(self)
        copy_args = self.make_args()
        if isinstance(value, str):
            # A string value means redefining the parameter_name.
            return cls(*copy_args, parameter_name=value)
        else:
            # Otherwise, value is a number-like object with which to multiply the angle.
            *gate_args, angle = copy_args
            return cls(*gate_args, angle * value)

    def make_args(self) -> tuple:
        """
        :return: the sequence of arguments that would be needed to instantiate a copy of self.
        """
        # Note that instantiating a copy of self also requires the keyword argument 'parameter'
        # if parameter is not None.
        args = super().make_args()
        return (*args, self.angle)

    def to_json(self) -> JSONType:
        """
        :return: a json compatible object with all the information about the gate.
        """
        args = self.make_args()
        if self.parameter_name is None:
            return json_wrap([type(self).__name__ + self._FIXED, *args])
        elif self.parameter_name == self._DEFAULT_PARAMETER_NAME:
            return json_wrap([type(self).__name__ + self._PARAMETRIZED, *args])
        else:
            # For gates with a non-standard parameter value we should include the parameter.
            return json_wrap([type(self).__name__, *args, self.parameter_name])

    @classmethod
    def from_json(cls, data) -> "Gate":
        class_name, *gate_data = data
        if isinstance(gate_data[-1], str):
            *gate_data, parameter_name = gate_data
        elif class_name.endswith(cls._PARAMETRIZED):
            parameter_name = cls._DEFAULT_PARAMETER_NAME
        else:
            parameter_name = None

        *qubit_data, angle = gate_data
        qubit_args = (Qubit(label) for label in qubit_data)
        return cls(*qubit_args, angle, parameter_name=parameter_name)

    def __repr__(self):
        arguments = ", ".join(repr(arg) for arg in self.make_args())
        if self.parameter_name is not None:
            arguments += f", parameter_name='{self.parameter_name}'"

        return f"{type(self).__name__}({arguments})"

    def __eq__(self, other):
        return super().__eq__(other) and (self.parameter_name == other.parameter_name)

    def __hash__(self):
        # Since we redefine __eq__, we should also explicitly redirect __hash__ to super(),
        # otherwise it will return None.
        # https://docs.python.org/3.9/reference/datamodel.html#object.__hash__
        return super().hash(self)


####################################################################################################


class X(Gate1):
    """Represents an X gate"""


class Y(Gate1):
    """Represents a Y gate"""


class Z(Gate1):
    """Represents a Z gate"""


class H(Gate1):
    """Represents a Hadamard gate"""


class CNOT(Gate2):
    """Represents a CNOT gate"""

    aliases = ("CX",)

    def __init__(self, control: Qubit, target: Qubit):
        """
        :param Qubit control: The qubit that controls whether the gate will act
               (if Z_control == -1) or not (if Z_control == 1).
        :param Qubit target: The qubit that will be flipped if Z_control == -1.
        """
        super().__init__(control, target)


class Rx(RMixin, Gate1):
    """Represents an RX gate"""


class Ry(RMixin, Gate1):
    """Represents an RY gate"""


class Rz(RMixin, Gate1):
    """Represents an RZ gate"""


class Rzz(RMixin, Gate2):
    """Represents an RZZ gate"""
