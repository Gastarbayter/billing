from decimal import Decimal

from billing.api import serializers
from billing.api.controllers.wallet import change_balance
from billing.db import models
from billing.db.engine import db
from billing.errors import exception
from billing.utils.constances import TransactionType


@db.transaction()
async def create_transfer(transfer: serializers.TransferRequests) -> dict:
    contains_transaction: bool = await models.Transactions.is_contains_transaction(transfer.transaction_code)

    if contains_transaction:
        raise exception.DuplicateTransactionExceptions()

    source_wallet_balance: int = await change_balance(wallet_id=transfer.source_wallet_id, amount=-transfer.amount)
    target_wallet_balance: int = await change_balance(wallet_id=transfer.target_wallet_id, amount=transfer.amount)

    transactions_type: dict = await models.Transactions.get_transaction_type(TransactionType.Transfer)

    history_id: int = await models.Transactions.save_history(
        source_wallet_id=transfer.source_wallet_id,
        target_wallet_id=transfer.target_wallet_id,
        transaction_type_id=transactions_type['transaction_type_id'],
        amount=transfer.amount,
        code=transfer.transaction_code,
    )

    return {
        **dict(transfer),
        'source_wallet_balance': source_wallet_balance,
        'target_wallet_balance': target_wallet_balance,
        'transaction_type_id': transactions_type['transaction_type_id'],
        'history_id': history_id,
    }


@db.transaction()
async def create_replenishment(replenishment: serializers.ReplenishmentRequests) -> dict:
    contains_transaction: bool = await models.Transactions.is_contains_transaction(replenishment.transaction_code)

    if contains_transaction:
        raise exception.DuplicateTransactionExceptions()

    wallet_balance: Decimal = await change_balance(wallet_id=replenishment.wallet_id, amount=replenishment.amount)

    transactions_type: dict = await models.Transactions.get_transaction_type(TransactionType.Replenishment)

    history_id: int = await models.Transactions.save_history(
        target_wallet_id=replenishment.wallet_id,
        transaction_type_id=transactions_type['transaction_type_id'],
        amount=replenishment.amount,
        code=replenishment.transaction_code,
    )
    return {
        **dict(replenishment),
        'transaction_type_id': transactions_type['transaction_type_id'],
        'balance': wallet_balance,
        'history_id': history_id,
    }
