import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", default="postgresql+asyncpg://psu:psu@db:5432/todos")


settings = Settings()
