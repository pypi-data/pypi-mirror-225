def test_get_locations_by_id(hh_client, test_data):
    response = hh_client.locations.get_locations(id=test_data.test_city_id)
    print(response)
    assert response[-1].name == test_data.test_city_name


def test_get_locations_by_name(hh_client, test_data):
    response = hh_client.locations.get_locations(name=test_data.test_city_name)
    assert response[-1].id == test_data.test_city_id
