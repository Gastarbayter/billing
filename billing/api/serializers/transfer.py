from decimal import Decimal
from uuid import UUID

from pydantic import (
    Field,
)

from billing.api.serializers.common import AmountModel


class TransferRequests(AmountModel):
    source_wallet_id: int = Field(
        alias='sourceWalletId',
        title='Идентифкатор кошелька с которого осуществляутся перевод',
    )
    target_wallet_id: int = Field(
        alias='targetWalletId',
        title='Идентифкатор кошелька на который осуществляется перевод',
    )


class TransferResponse(TransferRequests):
    transaction_type_id: int = Field(alias='transactionTypeId', title='Идентифкатор типа транзакции')
    transaction_code: UUID = Field(alias='transactionCode', title='Код транзакции')
    source_wallet_balance: Decimal = Field(
        alias='sourceWalletBalance',
        title='Баланс кошелька с которого осуществляутся перевод',
    )

    target_wallet_balance: Decimal = Field(
        alias='targetWalletBalance',
        title='Баланс кошелька на который осуществляется перевод',
    )

    class Config:
        allow_population_by_field_name = True
