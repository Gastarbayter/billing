from pydantic import (
    BaseModel,
    Field,
)


class ClientRequests(BaseModel):
    login: str = Field(min_length=1, title='Логин пользователя')
    first_name: str = Field(min_length=1, alias='firstName', title='Имя Клиента')
    last_name: str = Field(min_length=1, alias='lastName', title='Фамилия Клиента')
    passport_series: str = Field(min_length=4, max_length=10, alias='passportSeries', title='Серия паспорта')
    passport_number: str = Field(min_length=4, max_length=10, alias='passportNumber', title='Номер паспорта')


class ClientResponse(ClientRequests):
    client_id: int = Field(alias='clientId', title='Идентифкатор пользователя')
    wallet_id: int = Field(alias='walletId', title='Идентификатор кошелька клиента')

    class Config:
        allow_population_by_field_name = True
