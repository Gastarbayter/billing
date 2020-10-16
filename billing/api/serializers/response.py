from pydantic import (
    BaseModel,
    Field,
)


class ClientResponse(BaseModel):
    client_id: int = Field(alias='clientId', title='Идентифкатор пользователя')
    login: str = Field(min_length=1, title='Логин пользователя')
    first_name: str = Field(min_length=1, alias='firstName')
    last_name: str = Field(min_length=1, alias='LastName')
    passport_series: str = Field(min_length=4, max_length=10, alias='passportSeries')
    passport_number: int = Field(alias='passportNumber')
