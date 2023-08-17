"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Extensions to process the results from the ParityOS cloud services.
"""
import random
from abc import ABC
from itertools import combinations
from typing import Dict, List

from parityos.base import ParityOSException, Qubit


class ParityDecoderExtension(ABC):
    """
    Extends the ParityOSOutput class with the methods `decode`, `error_correct`,
    `select_reduced_readout_qubits` and `make_full_configuration_from_partial`.
    These methods can decode physical configurations into logical configurations.

    It is possible to use a partial read-out to construct a full physical configuration,
    based on the redundant encoding that the parity architecture offers. This is especially
    useful if only a limited number of qubits can be read out in the hardware setup, or if
    the read-out failed on some qubits.
    """

    def decode(self, configuration: Dict[Qubit, int]) -> List[Dict[Qubit, int]]:
        """
        Decodes a physical configuration back to a logical one, it is important that the
        configuration contains enough qubits to reconstruct the logical state. If not
        enough qubits are included, a ParityOSException will be raised.

        :param configuration: A physical configuration to decode, the keys are qubits
                              on the physical device, the values are either +1 or -1.

        :return: A list containing all equally-likely logical configuration that correspond to
                 the physical configuration.  Each logical configuration is a dictionary
                 going from qubit, to +1 or -1, similar to the physical configuration.
        """
        # If not all physical qubits are specified in the configuration, we deduce the value
        # of those qubits from the constraints.
        if len(configuration) != len(self.mappings.encoding_map):
            configuration = self.make_full_configuration_from_partial(configuration)

        # Now error correct the resulting configuration onto the physical code subspace.
        corrected_configurations = self.error_correct(configuration)

        logical_configurations = []
        for corrected_configuration in corrected_configurations:

            logical_configuration = {}
            for logical_qubit, parity_map in self.mappings.decoding_map.items():
                # The logical value is the parity of the decoding, times the product of all
                # the values of the physical qubits that encode this logical qubits.
                logical_value = parity_map.parity
                for physical_qubit in parity_map.qubits:
                    logical_value *= corrected_configuration[physical_qubit]

                logical_configuration[logical_qubit] = logical_value

            logical_configurations.append(logical_configuration)

        return logical_configurations

    def error_correct(self, configuration: Dict[Qubit, int]) -> List[Dict[Qubit, int]]:
        """
        Correct errors using the nearest neighbor algorithm

        :param configuration: a physical configuration to correct for errors

        :return: A list of possible physical configurations that satisfy all constraints
                 (and hence are part of the physical code subspace), which each were obtained
                 at the smallest possible Hamming distance from the original configuration.
        """
        # If we already have a valid codeword, we are done
        if self._check_parity(configuration):
            return [configuration]

        # Search the bitstring space by flipping k bits at a time, increasing k every step,
        # until we find a valid codeword.  We want to keep track of all valid codewords found
        # at the shortest distance k, since they are all equally likely.
        for k in range(1, len(self.mappings.encoding_map)):
            # Prepare a list to accumulate valid codewords
            valid_configurations = []

            # Look at every possible combination of k flipped bits
            for qubits_to_flip in combinations(self.mappings.encoding_map, k):
                flipped_configuration = configuration.copy()
                for qubit in qubits_to_flip:
                    flipped_configuration[qubit] *= -1

                if self._check_parity(flipped_configuration):
                    valid_configurations.append(flipped_configuration)

            # If any valid codewords were found, we can return them
            if valid_configurations:
                return valid_configurations

        raise ParityOSException("There are no valid codewords in the entire physical code space")

    def select_reduced_readout_qubits(self) -> List[Qubit]:
        """
        Constructs a random minimal list of qubits that can be read-out and still be used
        to recover the full logical configuration.

        Note that when these qubits are used for read-out, no error correction can be applied.

        :return: A random list of qubits that are selected for read-out.
        """
        # If there are no constraints in the compiled problem, we have to read out every qubit
        if not self.compiled_problem.constraints:
            return list(self.mappings.encoding_map.keys())

        constraint = random.choice(tuple(self.compiled_problem.constraints))

        # Start with all but one of the constraint qubits as the read-out set (the state of the
        # last qubit can always be found using the constraint).
        readout_qubits = list(constraint.qubits)[1:]

        # Make a configuration that has all the qubits that are known in it, the state of the
        # qubits does not matter.
        configuration = {q: 1 for q in constraint.qubits}

        # In this loop we keep iterating between deducing how far we can get from the current
        # set of qubits and then adding new qubits if we cannot deduce the state of all qubits
        # yet.
        configuration = self.make_full_configuration_from_partial(
            configuration, return_incomplete=True
        )

        while len(configuration) != len(self.mappings.encoding_map):
            # Find the next qubits to add to the read-out set based on the constraint
            # that has the minimum number of remaining unknowns
            qubits_to_add = self._find_next_readout_qubits(configuration)
            configuration.update({q: 1 for q in qubits_to_add})
            readout_qubits.extend(qubits_to_add)
            configuration = self.make_full_configuration_from_partial(
                configuration, return_incomplete=True
            )

        return readout_qubits

    def make_full_configuration_from_partial(
        self, configuration: Dict[Qubit, int], return_incomplete: bool = False
    ) -> Dict[Qubit, int]:
        """
        Reconstructs a full physical configuration from a partial one
        using the constraints in the compiled problem.

        :param configuration: A partial physical configuration to extend.
        :param return_incomplete: If this flag is set to True, we return a physical
                                  configuration even if the full configuration could not
                                  be reconstructed. The configuration returned in that case
                                  contains all the qubits that could be deduced.
        :return: Full physical configuration deduced from the parity constraints.
        """
        # This dictionary will be used to add all reconstructed values of the qubits, we start
        # from the given configuration.
        deduced_configuration = configuration.copy()

        # Make a list of the unknown qubits in all constraints, the goal is to remove all unknowns
        # from the constraints until we are finished, or can not make any more progress.
        unknowns_constraints = []
        for constraint in self.compiled_problem.constraints:
            parity = constraint.value
            unknown_constraint_qubits = []
            for qubit in constraint.qubits:
                if qubit in configuration:
                    parity *= configuration[qubit]
                else:
                    unknown_constraint_qubits.append(qubit)
            unknowns_constraints.append((unknown_constraint_qubits, parity))

        while unknowns_constraints:
            new_unknowns_constraints = []
            for constraint_qubits, parity in unknowns_constraints:
                new_constraint_qubits = []
                for qubit in constraint_qubits:
                    # If the qubit is already in the deduced configuration, we do not
                    # have to keep track of it anymore, we can multiply its state
                    # with the constraint parity and not add it to the new unknowns.
                    if qubit in deduced_configuration:
                        parity *= deduced_configuration[qubit]
                    else:
                        new_constraint_qubits.append(qubit)

                if len(new_constraint_qubits) == 1:
                    # If there is exactly one qubit left in the unknowns of this constraint,
                    # we now know its value to be equal to remaining parity, so we can add it
                    # to the deduced configuration.
                    deduced_configuration[new_constraint_qubits[0]] = parity
                elif len(new_constraint_qubits) == 0:
                    # If there are no unknowns left in the constraint, we simply do nothing.
                    # Note that if the remaining parity is -1, the read-out contains an error,
                    # but the purpose of this function is not to do error correction (that
                    # will be done later).
                    pass
                else:
                    # If there are still more than two unknown qubits in the constraint,
                    # we have to put it back into the unknown constraints.
                    new_unknowns_constraints.append((new_constraint_qubits, parity))

            if new_unknowns_constraints == unknowns_constraints:
                # We cannot make any further progress, after checking all constraints,
                # so reconstruction failed.
                if return_incomplete:
                    return deduced_configuration
                else:
                    raise ParityOSException("Decoding failed for the given read-out set")
            else:
                # If we made some progress, continue the algorithm
                unknowns_constraints = new_unknowns_constraints

        return deduced_configuration

    def _check_parity(self, configuration: Dict[Qubit, int]) -> bool:
        """
        Checks whether a configuration satisfies all the constraints

        :param configuration: A physical configuration to check.

        :return: True if it satisfies all constraints, False otherwise.
        """
        for constraint in self.compiled_problem.constraints:
            # Calculate the product of all the states of the qubits in the constraint
            constraint_qubits_product = 1
            for qubit in constraint.qubits:
                constraint_qubits_product *= configuration[qubit]

            if constraint_qubits_product != constraint.value:
                # Early abort if one of the constraints is not satisfied
                return False

        return True

    def _find_next_readout_qubits(self, configuration: Dict[Qubit, int]) -> List[Qubit]:
        """
        Helper method for select_random_reduced_readout_qubits. Selects a list of qubits
        that should be added to the read-out set. Go over all constraints in the compiled
        problem and select the constraint with the fewest number of unknowns. Then returns
        all but one of the qubits in that constraint.

        :param configuration: A dictionary containing all read-out qubits as well as all qubit
                              values that can be deduced from the read-out qubits.
        :return: A list of qubits that should be added to the read-out set.
        """
        min_number_unknowns = float("inf")
        best_qubits = None
        for constraint in self.compiled_problem.constraints:
            unknown_qubits = [qubit for qubit in constraint.qubits if qubit not in configuration]
            if unknown_qubits and len(unknown_qubits) < min_number_unknowns:
                best_qubits = unknown_qubits
                min_number_unknowns = len(unknown_qubits)

        return best_qubits[1:]
