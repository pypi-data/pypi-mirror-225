from dataclasses import dataclass, field
from datetime import timezone
from typing import TYPE_CHECKING, Any

from hollihop_api_client.base import BaseCategory
from hollihop_api_client.tools import dict_to_camel, dict_to_snake

if TYPE_CHECKING:
    from hollihop_api_client.api import AbstractAPI


@dataclass
class Office:
    id: None | int = None
    name: None | str = None
    location: None | str = None
    address: None | str = None
    email: None | str = None
    phone: None | str = None
    no_classrooms: None | bool = None
    time_zone: None | timezone = None
    license: None | str = None


@dataclass
class Offices:
    offices: list[Office] = field(default_factory=list)


class OfficesCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_offices(
            self,
            id: None | int = None,
            location_id: None | int = None,
            name: None | str = None,
            license: None | str = None
    ) -> list[Office]:
        data = dict_to_camel(self.handle_parameters(locals()))

        response = self.api.request(
            method='GetOffices',
            http_method='GET',
            data=data
        )

        response = dict_to_snake(response)

        return [Office(**_) for _ in Offices(**response).offices]

    def get_all_offices_name(self) -> list[str]:
        offices = self.get_offices()
        return [office.name for office in offices]

    def get_all_offices_id(self) -> list[int]:
        offices = self.get_offices()
        return [office.id for office in offices]


__all__ = ['OfficesCategory']
