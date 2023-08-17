"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Exceptions for errors in the ParityOS api_interface software.
"""


class ParityOSException(Exception):
    """
    General exception thrown by ParityOS.
    """

    pass


class ParityOSImportError(ImportError):
    """
    ImportError related to uninstalled optional ParityOS dependencies.
    """

    pass
