from typing import TYPE_CHECKING

from hollihop_api_client.methods import (EdUnitsCategory, LeadsCategory,
                                         LocationsCategory, OfficesCategory,
                                         StudentsCategory)

if TYPE_CHECKING:
    from hollihop_api_client.api import AbstractAPI


class APICategories:
    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    @property
    def locations(self) -> LocationsCategory:
        return LocationsCategory(self.api)

    @property
    def offices(self) -> OfficesCategory:
        return OfficesCategory(self.api)

    @property
    def ed_units(self) -> EdUnitsCategory:
        return EdUnitsCategory(self.api)

    @property
    def ed_unit_students(self) -> StudentsCategory:
        return StudentsCategory(self.api)

    @property
    def leads(self) -> LeadsCategory:
        return LeadsCategory(self.api)


__all__ = ['APICategories']
