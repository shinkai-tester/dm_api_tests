import time
import json
from hamcrest import assert_that, has_properties, equal_to
from requests import Response


class Assertions:
    def __init__(self, orm_db):
        self.orm_db = orm_db

    def assert_user_was_created(self, login):
        dataset = self.orm_db.get_user_by_login(login=login)
        for row in dataset:
            assert_that(row, has_properties(
                {
                    'Login': login,
                    'Activated': False
                }
            ))

    def assert_user_was_activated(self, login):
        def check_activation():
            data = self.orm_db.get_user_by_login(login=login)
            for r in data:
                if r.Activated:
                    return True
            return False

        end_time = time.time() + 5  # 5 seconds timeout
        while time.time() < end_time:
            if check_activation():
                break
            time.sleep(1)
        else:
            assert False, f'User {login} was not activated in time'

    @staticmethod
    def assert_error_user_creation(check: dict, response: Response):
        assert_that(response.json().get("errors"), equal_to(check))

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON should have key '{name}'. But it's not present"

    @staticmethod
    def get_value_from_structure(data, path=None):
        """Get a value from a nested structure (dict or object) based on a provided path."""
        if path:
            for key in path:
                if isinstance(data, dict):
                    data = data.get(key, {})
                else:  # if it's an object
                    data = getattr(data, key, {})
        return data

    def assert_json_value_by_name(self, response, name, expected_value, error_message, path=None):
        if isinstance(response, Response):
            data = response.json()
        else:
            data = response

        # Extract nested data if path is provided
        data = self.get_value_from_structure(data, path)

        # Check whether it's a dict or an object and get the value by name accordingly
        if isinstance(data, dict):
            assert name in data, f"Response JSON doesn't have key '{name}'"
            actual_value = data.get(name)
        else:  # if it's an object
            assert hasattr(data, name), f"Object doesn't have attribute '{name}'"
            actual_value = getattr(data, name)

        assert actual_value == expected_value, error_message
