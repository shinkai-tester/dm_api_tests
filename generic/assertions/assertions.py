import json
import time
from contextlib import contextmanager
import allure
import requests
from hamcrest import assert_that, has_properties, equal_to, has_entries
from requests import Response
from generic.helpers.orm_db import OrmDatabase


class Assertions:
    def __init__(self, orm_db: OrmDatabase):
        self.orm_db = orm_db

    def assert_user_was_created(self, login):
        with allure.step("Assert that the user has been created"):
            dataset = self.orm_db.get_user_by_login(login=login)
            for row in dataset:
                assert_that(row, has_properties(
                    {
                        'Login': login,
                        'Activated': False
                    }
                ))

    def assert_user_was_activated(self, login):
        with allure.step("Assert that the user has been activated"):
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

    @contextmanager
    def check_status_code_http(self, expected_status_code: requests.codes = requests.codes.OK,
                               expected_result: dict = {}):
        from dm_api_account import ApiException
        with allure.step('Check HTTP status code'):
            try:
                yield
            except ApiException as e:
                assert e.status == expected_status_code
                assert_that(json.loads(e.body)['errors'], has_entries(expected_result))
