from os import environ


class Settings:
    def __init__(self):
        self.DB_USER = environ.get("DB_USER")
        self.DB_PASS = environ.get("DB_PASS")
        self.DB_HOST = environ.get("DB_HOST")
        self.DB_PORT = environ.get("DB_PORT")
        self.DB_NAME = environ.get("DB_NAME")
        self.DB_URI = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
