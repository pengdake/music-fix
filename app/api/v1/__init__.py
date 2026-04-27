from fastapi import APIRouter
from .music import router as music_router

router = APIRouter()
router.include_router(music_router, prefix="/music", tags=["music"])