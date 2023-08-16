from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING, Any

import phonenumbers

from hollihop_api_client.base import BaseCategory
from hollihop_api_client.methods.ed_units import EdUnit
from hollihop_api_client.tools import dict_to_camel, dict_to_snake

if TYPE_CHECKING:
    from hollihop_api_client.api import AbstractAPI


def replace_spaces(from_str: str):
    return from_str.replace('\xa0', ' ')


@dataclass
class StudentAgent:
    first_name: None | str = None
    last_name: None | str = None
    middle_name: None | str = None
    who_is: None | str = None
    mobile: None | str = None
    use_mobile_by_system: None | str = None
    phone: None | str = None
    email: None | str = None
    use_email_by_system: None | bool = None
    skype: None | str = None
    job_or_study_place: None | str = None
    position: None | str = None
    is_customer: None | bool = None
    birthday: None | datetime = None


@dataclass
class Payer:
    client_id: int | None = None
    is_company: bool | None = None
    name: str | None = None
    actual: bool | None = None
    terminated_contracts: list = None
    price_id: int | None = None
    price_name: str | None = None
    discounts: list | None = None
    surcharges: list | None = None
    payable_minutes: int | None = None
    payable_units: str | None = None
    payable_minutes_ranged: int | None = None
    payable_units_ranged: str | None = None
    value: str | None = None
    value_ranged: str | None = None
    value_paid_ranged: str | None = None
    contract_value: str | None = None
    contract_value_restored: str | None = None
    contract_value_ranged: str | None = None
    contract_value_ranged_restored: str | None = None
    debt_date: datetime | None = field(init=True, default=None)
    ed_unit_payments: list | None = None

    def __post_init__(self):
        if self.debt_date:
            self.debt_date = datetime.fromisoformat(self.debt_date)
        if self.value:
            self.value = replace_spaces(self.value)
        if self.contract_value:
            self.contract_value = replace_spaces(self.contract_value)
        if self.contract_value_restored:
            self.contract_value_restored = replace_spaces(
                self.contract_value_restored)
        if self.price_name:
            self.price_name = replace_spaces(self.price_name)


def format_phone(number) -> str:
    return phonenumbers.format_number(
        phonenumbers.parse(number, 'RU'),
        phonenumbers.PhoneNumberFormat.E164
    )


@dataclass
class Student:
    ed_unit_id: int | None = None
    ed_unit_type: str | None = None
    ed_unit_name: str | None = None
    ed_unit_corporative: bool | None = None
    ed_unit_office_or_company_id: int | None = None
    ed_unit_office_or_company_name: str | None = None
    ed_unit_discipline: str | None = None
    ed_unit_level: str | None = None
    ed_unit_maturity: str | None = None
    ed_unit_learning_type: str | None = None
    student_client_id: int | None = None
    student_name: str | None = None
    student_mobile: str | None = None
    student_phone: str | None = None
    student_email: str | None = None
    student_agents: list[StudentAgent] | None = None
    student_extra_fields: list | None = None
    begin_date: datetime | None = None
    end_date: datetime | None = None
    begin_time: time | None = None
    end_time: time | None = None
    weekdays: int | None = None
    status: str | None = None
    study_minutes: int | None = None
    study_units: str | None = None
    days: list | None = None
    payers: list[Payer] | None = None
    phones: list[str] = field(init=False)

    def __post_init__(self):
        self.phones = []
        if self.payers:
            self.payers = [Payer(**_) for _ in self.payers]
        if self.student_agents:
            self.student_agents = [StudentAgent(
                **_) for _ in self.student_agents]
            for agent in self.student_agents:
                if agent.mobile:
                    self.phones.append(format_phone(
                        agent.mobile).replace('+', ''))
        if self.student_mobile:
            self.phones.append(format_phone(
                self.student_mobile).replace('+', ''))
        if self.student_phone:
            self.phones.append(format_phone(
                self.student_phone).replace('+', ''))
        if self.begin_date:
            self.begin_date = datetime.fromisoformat(self.begin_date)
        if self.end_date:
            self.end_date = datetime.fromisoformat(self.end_date)

    # def __repr__(self) -> str:
    #     return self.student_name


@dataclass
class Students:
    ed_unit_students: list[Student] = field(default_factory=list)


class StudentsCategory(BaseCategory):

    def __init__(self, api: 'AbstractAPI'):
        self.api = api

    def get_students(
            self,
            ed_unit_id: None | int = None,
            ed_unit_types: None | str = None,
            ed_unit_office_or_company_id: None | int = None,
            ed_unit_office_or_company: None | str = None,
            student_client_id: None | int = None,
            date_from: None | datetime = None,
            date_to: None | datetime = None,
            statuses: None | str = None,
            query_payers: None | bool = None,
            query_days: None | bool = None
    ) -> list[Student]:
        data = dict_to_camel(self.handle_parameters(locals()))
        print(data)

        response = self.api.request(
            method='GetEdUnitStudents',
            http_method='GET',
            data=data
        )

        response = dict_to_snake(response)

        return [Student(**_) for _ in Students(**response).ed_unit_students]

    def get_all_students_name(self, **kwargs) -> list[str]:
        students = self.get_students(**kwargs)
        return [student.student_name for student in students]

    def get_all_students_id(self, **kwargs) -> list[int]:
        students = self.get_students(**kwargs)
        return [student.student_client_id for student in students]

    def get_students_with_debt(
            self,
            ed_unit_id: int,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            **kwargs):
        students = self.get_students(
            date_from=date_from,
            date_to=date_to,
            ed_unit_id=ed_unit_id,
            query_payers=True,
            **kwargs
        )

        if date_from:
            students = filter(
                lambda student: student.payers[-1].debt_date > date_from, students)
        if date_to:
            students = filter(
                lambda student: student.payers[-1].debt_date <= date_to, students)

        return students


__all__ = ['StudentsCategory']
