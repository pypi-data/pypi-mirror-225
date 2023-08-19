def test_ed_unit_students(hh_client, test_data):
    response = hh_client.ed_unit_students.get_students(ed_unit_id=test_data.test_group_id)
    assert response[-1].student_name == test_data.test_student_name


def test_ed_unit_students_debt_date(hh_client, test_data):
    response = hh_client.ed_unit_students.get_students(
        ed_unit_id=test_data.test_group_id,
        query_payers=True
    )
    assert response[-1].payers[-1].debt_date == test_data.test_debt_date
