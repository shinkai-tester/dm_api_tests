import allure
import pytest


@allure.parent_suite("Tests for checking the method POST{host}/v1/account")
@allure.sub_suite("Positive and negative checks")
class TestPostV1Account:
    @allure.title("Check user registration and activation")
    def test_create_user_success(self, dm_api_facade, orm_db, data_helper, prepare_user, assertions):
        """Test the registration and activation of a new user, and assert their initial properties"""

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password
        )

        assertions.assert_user_was_created(login=login)
        orm_db.set_activated_flag_by_login(login=login)
        assertions.assert_user_was_activated(login=login)
        dm_api_facade.login.login_user(
            login=login,
            password=password
        )

    @allure.title("Test user registration validations: positive, short password, short login, invalid email")
    @pytest.mark.parametrize('login, email, password, status_code, check', [
        ('Sasha', 'Sasha_1234@example.com', 'Pass1234!', 201, ''),
        ('Sasha', 'Sasha_1234@example.com', 'Pass', 400, {"Password": ["Short"]}),
        ('s', 'Sasha_1234@example.com', 'Pass1234!', 400, {"Login": ["Short"]}),
        ('Sasha', 'Sasha_1234@', 'Pass1234!', 400, {"Email": ["Invalid"]}),
        ('Sasha', 'Sasha_1234example.com', 'Pass1234!', 400, {"Email": ["Invalid"]}),
    ])
    def test_user_creation_validations(self,
                                       dm_api_facade,
                                       orm_db,
                                       login,
                                       email,
                                       password,
                                       assertions,
                                       status_code,
                                       check,
                                       cleanup_user_and_emails
                                       ):

        """Test the user registration with various input combinations to validate error and success scenarios"""

        response = dm_api_facade.account.register_new_user(
            login=login,
            email=email,
            password=password,
            status_code=status_code
        )

        if status_code == 201:
            assertions.assert_user_was_created(login=login)
            orm_db.set_activated_flag_by_login(login=login)
            assertions.assert_user_was_activated(login=login)

            dm_api_facade.login.login_user(
                login=login,
                password=password
            )
        else:
            assertions.assert_json_value_by_name(
                response=response,
                name="errors",
                expected_value=check,
                error_message="Error is not the same as expected in test")
