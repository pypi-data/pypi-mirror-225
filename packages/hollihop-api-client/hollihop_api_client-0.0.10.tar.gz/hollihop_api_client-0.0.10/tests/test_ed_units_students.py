def test_ed_unit_students(hh_client, test_data):
    from pprint import pprint
    pprint(hh_client.ed_units.get_ed_unit_students(student_client_id=25759))
    pprint(hh_client.ed_units.get_ed_units(id=4536))
