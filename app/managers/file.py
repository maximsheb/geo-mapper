import os
import aiofiles

from uuid import UUID
from fastapi import UploadFile

from app.managers.geocoder import GeocoderManager
from app.models import LinkedDistance, GeoPoint
from app.utils.errors import (
    FileProcessingError,
    FileSaveError,
    FileReadError,
    FilePathError
)


class FileManager:
    CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB

    @classmethod
    async def read_in_chunks(cls, file_path: str) -> bytes:
        """
        Read file in chunks
        :param file_path: str path to csv file object
        :return: chunk of file in bytes limited by CHUNK_SIZE
        """
        try:
            async with aiofiles.open(file_path, 'rb') as file_object:
                while True:
                    chunk = await file_object.read(cls.CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk

        except FileNotFoundError:
            raise FilePathError(f"File {file_path} not found.")
        except OSError as e:
            raise FileReadError(f"Failed to read file {file_path}: {e}")
        except Exception as e:
            raise FileProcessingError(
                f"An unexpected error occurred "
                f"while reading the file {file_path}: {e}"
            )

    @classmethod
    async def save(cls, file: UploadFile):
        try:
            shared_dir = "/shared"
            file_path = os.path.join(shared_dir, file.filename)

            with open(file_path, "wb") as buffer:
                while chunk := await file.read(cls.CHUNK_SIZE):
                    buffer.write(chunk)
            return file_path

        except OSError as e:
            raise FileSaveError(f"Failed to save file {file.filename}: {e}")
        except Exception as e:
            raise FileProcessingError(
                f"An unexpected error occurred "
                f"while saving the file {file.filename}: {e}"
            )

    @classmethod
    async def process_chunk(
            cls,
            chunk: bytes,
            task_id: UUID,
    ) -> tuple[list[GeoPoint], list[LinkedDistance]]:
        """
        Process chunk of file and create geo points and linked distances
        :param chunk: bytes of file
        :param task_id: uuid of task
        :return: tuple of geo points and linked distances
        """
        geocoder_manager = GeocoderManager()

        chunk_str = chunk.decode('utf-8').splitlines()

        geo_points = await geocoder_manager.get_geo_points(chunk_str, task_id)
        linked_distances = await geocoder_manager.get_linked_distances(geo_points, task_id)  # noqa

        return geo_points, linked_distances
