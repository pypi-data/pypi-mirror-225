import os
from dataclasses import dataclass
from datetime import datetime

import pytest
from api import HolliHopAPI
from dotenv import load_dotenv


@dataclass
class TestData:
    test_city_name: str
    test_city_id: int
    test_office_name: str
    test_office_id: int
    test_student_name: str
    test_lead_name: str
    test_lead_id: int
    test_group_name: str
    test_group_id: int
    test_debt_date: datetime
    test_teacher_name: str
    test_teacher_id: int


@pytest.fixture()
def hh_client():
    load_dotenv()

    client = HolliHopAPI(
        domain=os.environ.get('HH_DOMAIN'),
        api_key=os.environ.get('HH_API_COMMON_KEY')
    )
    yield client


@pytest.fixture()
def test_data():
    load_dotenv()

    test_data = TestData(
        test_city_name=os.environ.get('TEST_CITY_NAME'),
        test_city_id=int(os.environ.get('TEST_CITY_ID')),
        test_office_name=os.environ.get('TEST_OFFICE_NAME'),
        test_office_id=int(os.environ.get('TEST_OFFICE_ID')),
        test_student_name=os.environ.get('TEST_STUDENT_NAME'),
        test_lead_name=os.environ.get('TEST_LEAD_NAME'),
        test_lead_id=int(os.environ.get('TEST_LEAD_ID')),
        test_group_name=os.environ.get('TEST_GROUP_NAME'),
        test_group_id=int(os.environ.get('TEST_GROUP_ID')),
        test_debt_date=datetime.fromisoformat(os.environ.get('TEST_DEBT_DATE')),
        test_teacher_name=os.environ.get('TEST_TEACHER_NAME'),
        test_teacher_id=int(os.environ.get('TEST_TEACHER_ID')),
    )

    yield test_data