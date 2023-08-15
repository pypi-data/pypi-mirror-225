from cooptools.geometry import Vector2
from cooptools.geometry import PolygonRegion
from cooptools.zones.logger import zoneLogger
from typing import List, Dict, Tuple
from cooptools.zones.exceptions import ZoneDoesntExistException, ZoneAlreadyExistsException

class ZoneManager:

    def __init__(self):
        self.zones: Dict[str, PolygonRegion] = {}

    def __getitem__(self, item):
        return self.zones[item]

    def __len__(self):
        return len(self.zones)

    def init_new_zone(self,
                      name: str,
                      initial_points: List[Vector2] = None,
                      override: bool = False):

        if name in self.zones and not override: raise ZoneAlreadyExistsException(name)

        self.zones[name] = PolygonRegion()

        if initial_points:
            self.zones[name].add_points(initial_points)

        zoneLogger.info(f"Zone {name} added")

    def delete_zone(self, zone_name: str):
        if zone_name not in self.zones:
            raise ZoneDoesntExistException(zone_name)

        del self.zones[zone_name]


    def add_to_zone(self, zone_name: str, point: Vector2, at_idx: int = None):
        z = self.zones.get(zone_name, None)

        if z is None: raise ZoneDoesntExistException(zone_name)

        z.add_points([point], at_idx=at_idx)
        zoneLogger.info(f"Point {point} added to zone '{zone_name}'")

    def remove_last_point_from_zone(self, zone_name: str):
        z = self.zones.get(zone_name, None)

        if z is None: raise ZoneDoesntExistException(zone_name)

        z.remove_point()
        zoneLogger.info(f"Point removed from zone '{zone_name}'")
        return True

    def member_zones(self, points: List[Vector2]) -> Dict[Vector2, List[str]]:
        member_zones = {}

        for point in points:
            members = []
            for id, zone in self.zones.items():
                if point.in_polygon(zone.boundary_points):
                    members.append(id)
            member_zones[point] = members

        return member_zones



