from decimal import Decimal
from uuid import UUID

from pydantic import (
    Field,
)

from billing.api.serializers.common import AmountModel


class ReplenishmentRequests(AmountModel):
    transaction_code: UUID = Field(alias='transactionCode', title='Код транзакции')
    wallet_id: int = Field(alias='walletId', title='Идентифкатор кошелька клиента')


class ReplenishmentResponse(ReplenishmentRequests):
    wallet_id: int = Field(alias='walletId', title='Идентифкатор кошелька клиента')
    transaction_type_id: int = Field(alias='transactionTypeId', title='Идентифкатор типа транзакции')
    balance: Decimal = Field(title='Баланс клиента')

    class Config:
        allow_population_by_field_name = True
