import pytest

from app import init_app
from settings import load_settings


@pytest.fixture
async def cli(loop, aiohttp_client):
    app = await init_app(load_settings())
    return await aiohttp_client(app)
