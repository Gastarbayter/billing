from enum import Enum


class TransactionType(Enum):
    Transfer = 'TRANSFER'
    Replenishment = 'REPLENISHMENT'
