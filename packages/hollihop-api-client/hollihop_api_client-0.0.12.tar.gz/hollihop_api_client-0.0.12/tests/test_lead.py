import json


def test_get_lead(hh_client, test_data):
    response = hh_client.leads.get_leads(id=test_data.test_lead_id)
    print(response[-1].agents)
    assert response[-1].name == test_data.test_lead_name


def test_add_lead(hh_client):
    response = hh_client.leads.add_lead(
        first_name='---',
        last_name='---',
        birthday='2023-01-01',
        office_or_company_id=3,
        status='Звонобот',
        ad_source='Звонобот',
        comment='Тестовый лид со Звонобота',
    )
    resp = hh_client.leads.edit_contacts(
        lead_id=response.lead_id,
        mobile='79226036452',

    )
    print(response)
