# This file is part of pyacoustid.
# Copyright 2011, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Example script that identifies metadata for files specified on the
command line.
"""

import os
import sys
from loguru import logger

import acoustid
from mutagen import File, MutagenError
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TXXX
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis


# API key for this demo script only. Get your own API key at the
# Acoustid Web for your application.
# http://acoustid.org/

API_KEY = "N6WLQOXT1O"
#API_KEY = "cSpUJKpD"


def get_metadata(filepath):
    results = acoustid.match(API_KEY, filepath)

    for score, rid, title, artist in results:
        logger.info(f"{artist} - {title}")
        logger.info(f"http://musicbrainz.org/recording/{rid}")
        logger.info(f"Score: {int(score * 100)}%")
        return {
            "artist": artist,
            "title": title,
            "score": int(score * 100),
            "MUSICBRAINZ_RECORDINGID": rid,
        }

def update_metadata(filepath):
    # This is a placeholder function. You can implement this function to
    # update the metadata of the file at 'filepath' using the information
    # in the 'metadata' dictionary returned by 'aidmatch'.
    audio_file = File(filepath)

    if audio_file is None:
        logger.error(f"Unsupported file format: {filepath}")
        return
    if isinstance(audio_file, MP3):
        audio = ID3(filepath)
        if "TXXX:MUSICBRAINZ_RECORDINGID" not in audio:
            metadata = get_metadata(filepath)
            if metadata is None:
                logger.error(f"Could not retrieve metadata for {filepath}")
                return
            audio_standard = EasyID3(filepath)
            audio_standard["title"] = metadata["title"]
            audio_standard["artist"] = metadata["artist"]
            audio_standard.save()
            audio.add(TXXX(encoding=3, desc="MUSICBRAINZ_RECORDINGID", text=metadata["MUSICBRAINZ_RECORDINGID"]))
        else:
            logger.info(f"MUSICBRAINZ_RECORDINGID already exists in {filepath}, skipping update.")
    elif isinstance(audio_file, FLAC):
        audio = FLAC(filepath)
        if "MUSICBRAINZ_RECORDINGID" not in audio:
            metadata = get_metadata(filepath)
            if metadata is None:   
                logger.error(f"Could not retrieve metadata for {filepath}")
                return
            audio["title"] = metadata["title"]
            audio["artist"] = metadata["artist"]
            audio["MUSICBRAINZ_RECORDINGID"] = metadata["MUSICBRAINZ_RECORDINGID"]
        else:
            logger.info(f"MUSICBRAINZ_RECORDINGID already exists in {filepath}, skipping update.")
    elif isinstance(audio_file, OggVorbis):
        audio = OggVorbis(filepath)
        if "MUSICBRAINZ_RECORDINGID" not in audio:
            metadata = get_metadata(filepath)
            if metadata is None:
                logger.error(f"Could not retrieve metadata for {filepath}")
                return
            audio["title"] = metadata["title"]
            audio["artist"] = metadata["artist"]
            audio["MUSICBRAINZ_RECORDINGID"] = metadata["MUSICBRAINZ_RECORDINGID"]
        else:
            logger.info(f"MUSICBRAINZ_RECORDINGID already exists in {filepath}, skipping update.")
    else:
        logger.error(f"Unsupported file format for metadata update: {filepath}")
        return
    audio.save()
    logger.info(f"Metadata updated for {filepath}")
     
def sync_music_metadata(music_dir):
    failed_files = []
    if not os.path.isdir(music_dir):
        logger.error(f"Provided path is not a directory: {music_dir}")
        return
    for root, _, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".flac", ".ogg")):
                filepath = os.path.join(root, file)
                logger.info(f"Processing file: {filepath}")
                try:
                    update_metadata(filepath)
                except MutagenError as mutagen_exc:
                    logger.error(f"Mutagen error processing file {filepath}: {mutagen_exc}")
                    failed_files.append(
                        {
                            "name": filepath.split("/")[-1].split(".")[0],
                            "filepath": filepath,
                            "error": f"Mutagen error: {mutagen_exc}"
                        }
                    )
                except acoustid.AcoustidError as acoustid_exc:
                    logger.error(f"AcoustID error processing file {filepath}: {acoustid_exc}")
                    failed_files.append(
                        {
                            "name": filepath.split("/")[-1].split(".")[0],
                            "filepath": filepath,
                            "error": f"AcoustID error: {acoustid_exc}"
                        }
                    )
                except Exception as exc:
                    logger.error(f"Error processing file {filepath}: {exc}")
                    failed_files.append(
                        {
                            "name": filepath.split("/")[-1].split(".")[0],
                            "filepath": filepath,
                            "error": str(exc)
                        }
                    )

    if failed_files:
        logger.error(f"Failed to process the following files: {failed_files}")
    return failed_files

if __name__ == "__main__":
    from core.logger import setup_logger
    setup_logger()
    music_dir = sys.argv[1]
    if not os.path.isdir(music_dir):
        logger.error(f"Provided path is not a directory: {music_dir}")
        sys.exit(1)
    for root, _, files in os.walk(music_dir):
        for file in files:
            if file.lower().endswith((".mp3", ".flac", ".ogg")):
                filepath = os.path.join(root, file)
                logger.info(f"Processing file: {filepath}")
                try:
                    update_metadata(filepath)
                except Exception as exc:
                    logger.error(f"Error processing file {filepath}: {exc}")
