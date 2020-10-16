import os

from pydantic import BaseSettings

ENVIRONMENT = os.environ['ENVIRONMENT'].upper()
CONFIG_FILE = os.environ.get('CONFIG_FILE', os.path.join('config', f'{ENVIRONMENT.lower()}.env'))
README_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'README.md',
)


class Settings(BaseSettings):
    APP_NAME: str

    DEBUG: bool
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DB_URL(self) -> str:
        return '{drivername}://{user}:{password}@{host}:{port}/{database}'.format(
            drivername='postgresql',
            user=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    README_PATH = README_PATH

    class Config:
        env_file = CONFIG_FILE
        env_file_encoding = 'utf-8'


settings = Settings()
