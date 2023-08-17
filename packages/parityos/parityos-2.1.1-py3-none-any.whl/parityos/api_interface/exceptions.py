"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Exceptions for errors from the ParityOS cloud services.
"""
from requests.exceptions import RequestException


class ParityOSAuthError(RequestException, ValueError):
    """
    Exception for failed logins to the ParityAPI server.
    """

    pass


class ParityOSRequestError(RequestException):
    """
    Exception for failed logins to the ParityAPI server.
    """

    pass
