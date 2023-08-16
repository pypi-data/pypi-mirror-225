from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

from hollihop_api_client.base import BaseCategory
from hollihop_api_client.tools import dict_to_camel, dict_to_snake, format_phone


if TYPE_CHECKING:
    from hollihop_api_client.api import AbstractAPI


@dataclass
class Agent:
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    is_customer: bool | None = None
    who_is: str | None = None
    email: str | None = None
    use_email_by_system: bool | None = None
    phone: str | None = None
    mobile: str | None = None
    use_mobile_by_system: bool | None = None
    job_or_study_place: str | None = None
    position: str | None = None
    birthday: datetime | None = None
    skype: str | None = None

    def __post_init__(self):
        if not self.phone is None:
            self.phone = format_phone(self.phone.replace('+', ''))


@dataclass
class ExtraField:
    name: str | None = None
    value: str | None = None


@dataclass
class Lead:
    id: int | None
    created: datetime | None = None
    updated: datetime | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    address_date: datetime | None = None
    ad_source: str | None = None
    status_id: str | None = None
    status: str | None = None
    birthday: datetime | None = None
    phone: str | None = None
    mobile: str | None = None
    use_mobile_by_system: bool | None = None
    email: str | None = None
    use_email_by_system: bool | None = None
    maturity: str | None = None
    learning_type: str | None = None
    discipline: str | None = None
    level: str | None = None
    agents: list[Agent] | None = None
    offices_and_companies: list | None = None
    assignees: list | None = None
    extra_fields: list | None = None
    student_client_id: int | None = None
    name: str = field(init=False)

    def __post_init__(self):
        self.name = ' '.join(filter(lambda str_obj: str_obj, [
                             self.last_name, self.first_name, self.middle_name]))
        if self.agents:
            self.agents = [Agent(**_) for _ in self.agents]
        if self.extra_fields:
            self.extra_fields = [ExtraField(**_) for _ in self.extra_fields]
        if not self.mobile is None:
            self.mobile = format_phone(self.mobile.replace('+', ''))
        if not self.phone is None:
            self.phone = format_phone(self.phone.replace('+', ''))


@dataclass
class Leads:
    leads: None | list[Lead] = field(default_factory=list)
    now: None | datetime = None


class LeadsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_leads(
            self,
            id: None | int = None,
            attached: None | bool = None,
            student_client_id: None | int = None,
            office_or_company_id: int | None = None,
            created_from: datetime | None = None,
            take: int | None
    ) -> list[Lead]:
        data = dict_to_camel(self.handle_parameters(locals()))

        response = self.api.request(
            method='GetLeads',
            http_method='GET',
            data=data
        )

        response = dict_to_snake(response)

        raw_leads = [Lead(**_) for _ in Leads(**response).leads]

        return raw_leads

    def get_all_leads_id(self, **kwargs) -> list[int]:
        leads = self.get_leads(**kwargs)
        return [lead.student_client_id for lead in leads]


__all__ = ['LeadsCategory']
