import asyncio

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: AnyUrl = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/testapp"
    )
    POSTGRES_TEST_URL: AnyUrl = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/test_testapp"
    )

    class Config:

        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()


async def async_get_settings() -> Settings:
    event_loop = asyncio.get_event_loop()
    return await event_loop.run_in_executor(None, get_settings)
