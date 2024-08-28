import asyncio
import csv
import ssl
import certifi

from uuid import UUID
from geopy import Nominatim, Location
from geopy.distance import geodesic

from app.models import GeoPoint, LinkedDistance


ssl_context = ssl.create_default_context(cafile=certifi.where())
geolocator = Nominatim(user_agent="geo-mapper", ssl_context=ssl_context)


class GeocoderManager:
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
    async def get_address_by_coords(cls, chunk: list[str]) -> tuple:
        """
        Get address by coordinates
        :param chunk: list of latitude and longitude for address search
        :return: address of the point
        """
        reader = csv.DictReader(chunk)

        geocode_tasks = [
            cls.reverse_geocode_async(
                float(row["Latitude"]), float(row["Longitude"]))  # noqa
            for row in reader
        ]
        return await asyncio.gather(*geocode_tasks)

    @classmethod
    async def get_geo_points(
            cls, chunk: list[str],
            task_id: UUID
    ) -> list[GeoPoint]:
        """
        Get geo points by addresses
        :param chunk: list of latitude and longitude for address search
        :param task_id: uuid of task
        :return: list of geo points
        """
        geo_points = []
        addresses = await cls.get_address_by_coords(chunk)
        reader = csv.DictReader(chunk)

        for index, row in enumerate(reader):
            geo_point = GeoPoint(
                name=row["Point"],
                latitude=float(row["Latitude"]),
                longitude=float(row["Longitude"]),
                address=addresses[index].address,
                task_id=task_id
            )
            geo_points.append(geo_point)
        return geo_points

    @classmethod
    async def get_linked_distances(
            cls, geo_points: list[GeoPoint],
            task_id: UUID
    ) -> list[LinkedDistance]:
        """
        Get linked distances by geo points
        :param geo_points: list of geo points
        :param task_id: uuid of task
        :return: list of linked distances
        """
        linked_distances = []

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
        return linked_distances
