import asyncio
import csv
import os
import ssl
import tempfile

import aiofiles
import certifi

from uuid import UUID

from fastapi import UploadFile
from geopy import Location
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from app.models import LinkedDistance, GeoPoint

ssl_context = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent="geo-mapper", ssl_context=ssl_context)


class FileManager:
    CHUNK_SIZE = 5 * 1024 * 1024  # 5 MB

    @classmethod
    async def reverse_geocode_async(cls, lat: float, lon: float) -> Location:
        """
        Reverse geocode the given latitude and longitude
        :param lat: latitude of the point in float
        :param lon: longitude of the point in float
        :return: address of the point
        """
        return await asyncio.to_thread(
            geolocator.reverse, (lat, lon), timeout=10
        )

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
            raise RuntimeError(f"File {file_path} not found.")
        except OSError as e:
            raise RuntimeError(f"Failed to read file {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(
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
            raise RuntimeError(f"Failed to save file {file.filename}: {e}")
        except Exception as e:
            raise RuntimeError(
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
        geo_points = []
        linked_distances = []

        chunk_str = chunk.decode('utf-8').splitlines()
        reader = csv.DictReader(chunk_str)

        geocode_tasks = [
            cls.reverse_geocode_async(
                float(row["Latitude"]), float(row["Longitude"]))  # noqa
            for row in reader
        ]
        addresses = await asyncio.gather(*geocode_tasks)

        del reader
        reader = csv.DictReader(chunk_str)

        # create geo points objects
        for index, row in enumerate(reader):
            geo_point = GeoPoint(
                name=row["Point"],
                latitude=float(row["Latitude"]),
                longitude=float(row["Longitude"]),
                address=addresses[index].address,
                task_id=task_id
            )
            geo_points.append(geo_point)

        # create linked distance objects
        for i in range(len(geo_points)):
            for j in range(i + 1, len(geo_points)):
                point1, point2 = geo_points[i], geo_points[j]
                distance = geodesic((point1.latitude, point1.longitude),
                                    (point2.latitude, point2.longitude)).meters
                linked_distance = LinkedDistance(
                    name=f"{point1.name}{point2.name}",
                    distance=distance,
                    task_id=task_id
                )
                linked_distances.append(linked_distance)

        return geo_points, linked_distances


file_manager = FileManager()
