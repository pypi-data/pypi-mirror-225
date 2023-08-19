from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from hollihop_api_client.base import BaseCategory
from hollihop_api_client.tools import dict_to_camel, dict_to_snake

if TYPE_CHECKING:
    from hollihop_api_client.api import AbstractAPI


@dataclass
class Location:
    id: None | int
    name: None | str


@dataclass
class Locations:
    locations: list[Location] = field(default_factory=list)


class LocationsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_locations(
            self,
            id: None | int = None,
            name: None | str = None
    ) -> list[Location]:
        data = dict_to_camel(self.handle_parameters(locals()))

        response = self.api.request(
            method='GetLocations',
            http_method='GET',
            data=data
        )

        response = dict_to_snake(response)

        return [Location(**_) for _ in Locations(**response).locations]

    def get_all_locations_name(self) -> list[str]:
        locations = self.get_locations()
        return [location.name for location in locations]

    def get_all_locations_id(self) -> list[int]:
        locations = self.get_locations()
        return [location.id for location in locations]


__all__ = ['LocationsCategory']
