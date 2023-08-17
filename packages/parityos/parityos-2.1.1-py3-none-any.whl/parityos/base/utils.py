"""
ParityQC GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2023.
All rights reserved.

Tools that can be used to serialize, deserialize, load and save ParityOS.base objects.
"""

from abc import abstractmethod, ABC
from ast import literal_eval
import pprint
from numbers import Integral
from typing import Any, Collection, Dict, Hashable, Iterable, List, Mapping, Sequence, Union


JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
# This is not an exact definition, but useful enough for type hinting.
# See the discussion at https://github.com/python/typing/issues/182
JSONMappingType = Mapping[str, JSONType]


def json_wrap(item) -> JSONType:
    """
    Converts an item to the corresponding json representation.
    :param item: The item to convert to json

    Unordered sequences (e.g. sets) are converted to sorted list,
    such that the JSON output will always be the same if the same set is provided.

    Note that this is not a fully json compliant converter.
    E.g. `None` values are not translated to `null`,
    and boolean types are converted to 0 or 1 instead of 'false' or 'true'.
    """
    if hasattr(item, "to_json"):  # e.g. a Qubit instance
        return item.to_json()
    elif isinstance(item, str):
        return item
    elif isinstance(item, Integral):  # integer-like numbers
        # Officially JSON does not distinguish between integers and floats, but we do in order
        # to make the JSON output more readable.
        return int(item)
    elif isinstance(item, Dict):
        # JSON requires strings as keys in a dictionary.
        # Note that here an integer 1 or a string '1' will result in the same key '1'.
        return {str(key): json_wrap(value) for key, value in item.items()}
    elif isinstance(item, Sequence):  # e.g. a label (1, 2)
        return [json_wrap(element) for element in item]
    elif isinstance(item, Collection):  # e.g. a set {2, 5, 4}
        return sorted(json_wrap(element) for element in item)
    elif isinstance(item, Iterable):  # e.g. a generator (qubit.label for qubit in qubits)
        return [json_wrap(element) for element in item]
    else:  # e.g. float or numpy types
        return float(item)


def dict_filter(mapping: Mapping, keys: Collection[Hashable]) -> dict:
    """Filter a mapping on a collection of keys.

    :param mapping: a dictionary or mapping of key:value pairs
    :param keys: a collection of keys
    :return: a filtered dictionary containing only the keys that are both in the original
             mapping and in the collection of keys.
    """
    return {key: mapping[key] for key in set(mapping).intersection(keys)}


class JSONLoadSaveMixin(ABC):
    """
    Mixin class that adds load and save methods.

    `load` instantiates an object by loading the JSON representation from a file.
    `save` writes a JSON representation to file.
    """

    @classmethod
    @abstractmethod
    def from_json(cls, data: JSONType):  # -> 'Self':  # Python 3.10 annotation
        """
        Constructs an instance from JSON data.

        :param data: a JSON-like list or dict
        :return: an instance of the class
        """

    @abstractmethod
    def to_json(self) -> JSONType:
        """
        Converts the instance to a json-compatible builtin Python object (float, str, list or dict).

        :return: the instance in json-serializable format
        """

    @classmethod
    def load(cls, filename):  # -> 'Self':  # Python 3.10 annotation
        """
        Instantiate an object using data read from a file in JSON compatible format.

        :param str filename: Name of the file that contains the JSON data.
        :returns: an instance of the class
        """
        with open(filename, "r") as file:
            data_string = file.read()

        data = literal_eval(data_string)
        return cls.from_json(data)

    def save(self, filename: str):
        """
        Save the object to file in JSON compatible format.

        :param filename: Name of the file where the JSON data will be stored.
        """
        data = self.to_json()
        # Officially JSON uses double quotes, therefore we replace single by double quotes.
        pretty_print_data = pprint.pformat(data).replace("'", '"')
        with open(filename, "w") as file:
            file.write(pretty_print_data)
