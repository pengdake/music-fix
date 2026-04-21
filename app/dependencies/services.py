

from app.services.music import MusicService
from fastapi import Request, Depends
from app.core.cache import Cache

def get_cache(request: Request)-> Cache:
    return request.app.state.cache

def get_music_service(cache: Cache = Depends(get_cache)) -> MusicService:
    return MusicService(cache)