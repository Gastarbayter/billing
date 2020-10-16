class BaseError(Exception):
    status_code: int = 500

    def __init__(self, message: str = None, detail: str = None):
        super().__init__(message)

        self.message = message
        self.detail = detail

    def __str__(self) -> str:
        return f'message: {self.message}, detail: {self.detail}'


class DuplicateClientExceptions(BaseError):
    status_code: int = 400
    message: str = 'A client with this data already exists'

    def __init__(self, *args, **kwarg):
        super().__init__(self.message, *args, **kwarg)


class BalanceExceptions(BaseError):
    status_code: int = 400
    message: str = 'Invalid client balance'

    def __init__(self, *args, **kwarg):
        super().__init__(self.message, *args, **kwarg)


class WalletNotFoundExceptions(BaseError):
    status_code: int = 404
    message: str = 'Wallet id: {wallet_id} not found'

    def __init__(self, wallet_id: int, *args, **kwarg):
        super().__init__(self.message.format(wallet_id=wallet_id), *args, **kwarg)
