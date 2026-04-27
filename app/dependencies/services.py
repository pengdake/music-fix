

from app.services.music import MusicService
from fastapi import Request, Depends
from app.core.cache import Cache

def get_cache(request: Request)-> Cache:
    return request.app.state.cache

def get_write_db(request: Request):
    db = request.app.state.write_session_local()
    try:
        yield db
    finally:
        db.close()

def get_read_db(request: Request):
    db = request.app.state.read_session_local()
    try:
        yield db
    finally:
        db.close()

def get_music_service(cache: Cache = Depends(get_cache)) -> MusicService:
    return MusicService(cache)