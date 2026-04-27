from app.dependencies.services import get_music_service
from app.schemas.common import ResponseModel
from app.schemas.music import MusicMetadata
from app.services.music import MusicService
from fastapi import File, UploadFile, APIRouter, Depends, HTTPException, status
from typing import Annotated


router = APIRouter()

@router.post(
    "/identify", 
    response_model=ResponseModel[MusicMetadata],
    summary="Identify a music file and return its metadata",
    description="This endpoint accepts a music file, identifies it using the AcoustID service, and returns the metadata including artist, title, score, and MusicBrainz recording ID.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Metadata retrieved successfully"},
        400: {"description": "Bad request, e.g., no file uploaded or invalid file format"},
        404: {"description": "Could not identify the music file."},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    }
)
async def get_metadata(file: Annotated[UploadFile, File(..., description="The music file to get metadata")], music_service: MusicService = Depends(get_music_service)):
    """Endpoint to identify a music file and return its metadata."""
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded.")
    if not file.filename.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format.")
    response = await music_service.get_metadata(file)
    if response.code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response.message)
    return response

