from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    validator,
)


class AmountModel(BaseModel):
    amount: Decimal = Field(title='Величина перевода')

    @validator('amount')
    def check_amount(cls, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError('amount должен быть положительным числом')
        return amount
