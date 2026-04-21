
from aiofiles import tempfile
from app.core.cache import Cache
from app.schemas.common import ResponseModel
from app.schemas.music import MusicMetadata
from app.utils.acoustid import get_metadata
from fastapi import UploadFile 
import os
import asyncio


class MusicService:
    def __init__(self, cache: Cache):
        self.cache = cache

    async def get_metadata(self, file: UploadFile):
        file_key = f"music_metadata:{file.filename}"
        cached_metadata = await self.cache.get(file_key)
        if cached_metadata:
            music_metadata = MusicMetadata.model_validate(cached_metadata)  # Validate the cached data against the MusicMetadata schema
            return ResponseModel[
                MusicMetadata
            ].success(
                message="Metadata retrieved successfully",
                data=music_metadata
            )
        async with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            await tmp.write(content)
        tmp_path = tmp.name
        metadata = await asyncio.to_thread(get_metadata, tmp_path)
        if metadata is None:
            return ResponseModel[
                MusicMetadata
            ](
                code=404,
                message="Could not identify the music file.",
                data=None
            )
        await self.cache.set(file_key, metadata)
        music_metadata = MusicMetadata.model_validate(metadata)  # Validate the metadata against the MusicMetadata schema
        os.remove(tmp_path)
        return ResponseModel[
            MusicMetadata
        ].success(
            message="Metadata retrieved successfully",
            data=music_metadata
        )

