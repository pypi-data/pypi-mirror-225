def test_get_ed_unit_by_id(hh_client, test_data):
    response = hh_client.ed_units.get_ed_units(id=test_data.test_group_id)
    assert response[-1].name == test_data.test_group_name


def test_get_ed_unit_by_teacher_id(hh_client, test_data):
    response = hh_client.ed_units.get_ed_units(teacher_id=test_data.test_teacher_id)
    assert response[-1].name == test_data.test_group_name


def test_get_ed_units_by_location_id(hh_client, test_data):
    response = hh_client.ed_units.get_ed_units(location_id=test_data.test_city_id)
    ed_units = list(filter(lambda ed_unit: ed_unit.name == test_data.test_group_name, response))
    assert ed_units[-1].name == test_data.test_group_name


def test_get_ed_units_by_office_id(hh_client, test_data):
    response = hh_client.ed_units.get_ed_units(office_or_company_id=test_data.test_office_id)
    ed_units = list(filter(lambda ed_unit: ed_unit.name == test_data.test_group_name, response))
    assert ed_units[-1].name == test_data.test_group_name
