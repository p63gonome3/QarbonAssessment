import requests


class TestPlaceGroup:
    def test_should_pass_given_valid_values(self):
        response = requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 0, "y": 3, "face": "SOUTH"}
            )
        expected_msg = "Toy model placed."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg

    def test_should_fail_given_negative_coord_value(self):
        response = requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": -1, "y": 0, "face": "SOUTH"}
            )
        error_response = response.json().get("detail")[0]
        expected_msg = "Input should be greater than or equal to 0"
        assert response.status_code == 422
        assert error_response.get("msg") == expected_msg

    def test_should_fail_given_coord_value_greater_than_board(self):
        response = requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 2, "y": 10, "face": "SOUTH"}
            )
        error_response = response.json().get("detail")[0]
        expected_msg = "Input should be less than or equal to 5"
        assert response.status_code == 422
        assert error_response.get("msg") == expected_msg

    def test_should_fail_given_incorrect_face_value(self):
        response = requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 3, "y": 1, "face": "test"}
            )
        error_response = response.json().get("detail")[0]
        expected_msg = "Input should be 'NORTH', 'EAST', 'SOUTH' or 'WEST'"
        assert response.status_code == 422
        assert error_response.get("msg") == expected_msg

    def test_should_fail_given_incomplete_parameters(self):
        response = requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 1, "y": 5}
            )
        error_response = response.json().get("detail")[0]
        expected_msg = "Field required"
        assert response.status_code == 422
        assert error_response.get("msg") == expected_msg


class TestMoveGroup:
    def test_should_fail_given_toy_not_in_place(self):
        requests.delete(
        "http://localhost:8000/remove/",
        headers={"ContentType": "application/json"}
        )
        response = requests.post(
            "http://localhost:8000/move/",
            headers={"ContentType": "application/json"}
            )
        expected_msg = "Toy model not placed yet."
        assert response.status_code == 400
        assert response.json().get("detail") == expected_msg

    def test_should_pass_given_valid_toy_movement(self):
        requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 3, "y": 3, "face": "SOUTH"}
            )
        response = requests.post(
            "http://localhost:8000/move/",
            headers={"ContentType": "application/json"}
            )
        expected_msg = "Toy model moved one unit forward."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg

    def test_should_pass_given_invalid_toy_movement(self):
        requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 0, "y": 0, "face": "SOUTH"}
            )
        response = requests.post(
            "http://localhost:8000/move/",
            headers={"ContentType": "application/json"}
            )
        expected_msg = "Toy model did not move."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg


class TestLeftGroup:
    def test_should_fail_given_toy_not_in_place(self):
        requests.delete(
        "http://localhost:8000/remove/",
        headers={"ContentType": "application/json"}
        )
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model not placed yet."
        assert response.status_code == 400
        assert response.json().get("detail") == expected_msg

    def test_should_pass_for_rotate_left(self):
        requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 3, "y": 3, "face": "SOUTH"}
            )
        response = requests.post(
            "http://localhost:8000/left/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model rotated 90deg to the left."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model placed at (3, 3) facing EAST."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg


class TestRightGroup:
    def test_should_fail_given_toy_not_in_place(self):
        requests.delete(
        "http://localhost:8000/remove/",
        headers={"ContentType": "application/json"}
        )
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model not placed yet."
        assert response.status_code == 400
        assert response.json().get("detail") == expected_msg

    def test_should_pass_for_rotate_right(self):
        requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 3, "y": 3, "face": "SOUTH"}
            )
        response = requests.post(
            "http://localhost:8000/right/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model rotated 90deg to the right."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model placed at (3, 3) facing WEST."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg


class TestReportGroup:
    def test_should_fail_given_toy_not_in_place(self):
        requests.delete(
        "http://localhost:8000/remove/",
        headers={"ContentType": "application/json"}
        )
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model not placed yet."
        assert response.status_code == 400
        assert response.json().get("detail") == expected_msg

    def test_should_pass_for_generate_toy_model_report(self):
        requests.post(
            "http://localhost:8000/place/",
            headers={"ContentType": "application/json"},
            json={"x": 3, "y": 3, "face": "SOUTH"}
            )
        response = requests.get(
            "http://localhost:8000/report/",
            headers={"ContentType": "application/json"},
            )
        expected_msg = "Toy model placed at (3, 3) facing SOUTH."
        assert response.status_code == 200
        assert response.json().get("message") == expected_msg


def test_should_pass_for_remove_toy_model_instance():
    response = requests.delete(
        "http://localhost:8000/remove/",
        headers={"ContentType": "application/json"}
        )
    expected_msg = "Toy model instance removed."
    assert response.status_code == 200
    assert response.json().get("message") == expected_msg
