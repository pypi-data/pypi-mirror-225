def test_get_offices_by_location_id(hh_client, test_data):
    response = hh_client.offices.get_offices(
        location_id=test_data.test_city_id)
    for office in response:
        assert office.location == test_data.test_city_name


def test_get_offices_by_location_name(hh_client, test_data):
    response = hh_client.offices.get_offices(name='Екатеринбург')
    print(response)
    for office in response:
        assert office.location == test_data.test_city_name


def test_get_office_by_id(hh_client, test_data):
    response = hh_client.offices.get_offices(id=test_data.test_office_id)
    assert response[-1].name == test_data.test_office_name
