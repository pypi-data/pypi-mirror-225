def test_get_lead(hh_client, test_data):
    response = hh_client.leads.get_leads(id=test_data.test_lead_id)
    assert response[-1].name == test_data.test_lead_name