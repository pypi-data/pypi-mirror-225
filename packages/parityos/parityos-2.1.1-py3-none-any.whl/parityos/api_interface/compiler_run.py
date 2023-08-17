"""
Parity Quantum Computing GmbH
Rennweg 1 Top 314
6020 Innsbruck, Austria

Copyright (c) 2020-2022.
All rights reserved.

Tools to process the results from the ParityOS cloud service.
"""
from enum import Enum

from parityos.base import JSONMappingType


class CompilerRun:
    """
    Encapsulates a compiler run; has attributes which describe relevant times
    at which they were submitted, started, and eventually finished or failed
    (in which case, a reason for failure is also given).
    """

    def __init__(
        self,
        id,
        submission_id,
        status,
        submitted_at,
        started_at=None,
        finished_at=None,
        failed_at=None,
        failure_reason=None,
    ):
        """
        :param id: id of the compiler run in ParityOS cloud database
        :param submission_id: id of the submission which triggered compile run
        :param status: status of the submission; see CompilerRunStatus enum
        :param submitted_at: time at which run was queued for execution
        :param started_at: time at which run started being executed
        :param finished_at: time at which run was completed
        :param failed_at: time at which run failed
        :param failure_reason: reason for which run failed
        """
        self.id = id
        self.submission_id = submission_id
        self.status = CompilerRunStatus(status)
        self.submitted_at = submitted_at
        self.started_at = started_at
        self.finished_at = finished_at
        self.failed_at = failed_at
        self.failure_reason = failure_reason

    @classmethod
    def from_json(cls, data: JSONMappingType) -> "CompilerRun":
        """
        Creates a CompilerRun object from a JSON-like data dictionary.
        :return: a CompilerRun object
        """
        return cls(**data)

    def __repr__(self):
        args = (
            self.id,
            self.submission_id,
            self.status.value,
            self.submitted_at,
            self.started_at,
            self.finished_at,
            self.failed_at,
            self.failure_reason,
        )
        return f"{self.__class__.__name__}{args}"


class CompilerRunStatus(Enum):
    """
    Enum for compiler run status.
    """

    SUBMITTED = "S"
    RUNNING = "R"
    COMPLETED = "C"
    FAILED = "F"
