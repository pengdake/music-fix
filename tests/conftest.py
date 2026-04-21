import fakeredis
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

@pytest.fixture
async def redis_client():
    return await fakeredis.aioredis.FakeRedis(decode_responses=True)

@pytest.fixture
async def cache(redis_client):
    from app.core.cache import Cache
    return Cache(redis_client)

@pytest.fixture
async def music_service(cache):
    from app.services.music import MusicService
    return MusicService(cache)

@pytest.fixture
async def upload_file():
    from fastapi import UploadFile
    from io import BytesIO
    dummy_music_content = b"fake mp3 binary data"  # This is just a header for a WAV file
    mock_file = BytesIO(dummy_music_content)
    return UploadFile(filename="test_music.wav", file=mock_file)

@pytest.fixture
async def async_client():
    from app.main import app
    transport = ASGITransport(app=app) 
    async with AsyncClient(transport=transport, base_url="http://async-test") as client:
        yield client

@pytest.fixture()
async def client():
    from app.main import app
    with TestClient(app, base_url="http://test") as client:
        yield client