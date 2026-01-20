from enum import Enum


class ContractStatus(str, Enum):
    CREATED = "CREATED"
    APPROVED = "APPROVED"
    SENT = "SENT"
    SIGNED = "SIGNED"
    LOCKED = "LOCKED"
    REVOKED = "REVOKED"


ALLOWED_TRANSITIONS = {
    ContractStatus.CREATED: {ContractStatus.APPROVED, ContractStatus.REVOKED},
    ContractStatus.APPROVED: {ContractStatus.SENT},
    ContractStatus.SENT: {ContractStatus.SIGNED, ContractStatus.REVOKED},
    ContractStatus.SIGNED: {ContractStatus.LOCKED},
    ContractStatus.LOCKED: set(),
    ContractStatus.REVOKED: set(),
}


def validate_transition(current: ContractStatus, target: ContractStatus) -> bool:
    """
    Returns True if transition is allowed, otherwise False.
    """
    return target in ALLOWED_TRANSITIONS[current]
