import pytest

from app import init_app
from settings import load_settings


@pytest.fixture
async def cli(loop, aiohttp_client):
    settings = load_settings()
    db = settings['redis']['REDIS_TEST_DB']
    app = await init_app(settings, db)
    return await aiohttp_client(app)
