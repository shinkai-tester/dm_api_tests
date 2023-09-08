from hamcrest import has_properties, assert_that, greater_than_or_equal_to, all_of, only_contains, has_length
from dm_api_account.models.roles import UserRole
from generic.helpers.data_generator import DataGeneratorHelper
from services.dm_api_account import Facade


def test_put_v1_account_email():
    """Test the process of changing a user's email and re-activating the account."""

    # Initialize helper and API client
    data_helper = DataGeneratorHelper()
    api = Facade(host="http://5.63.153.31:5051")

    # Generate user data
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()

    # Register and activate user
    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )
    api.account.activate_registered_user(login=login)

    # Change user's email
    response_change_email = api.account.change_user_email(
        login=login,
        password=password,
        email=data_helper.generate_email()
    )
    assert_that(response_change_email.resource, has_properties(
        {
            "login": login,
            "roles": all_of(only_contains(
                UserRole.GUEST,
                UserRole.PLAYER,
                UserRole.ADMIN,
                UserRole.NANNY_MODERATOR,
                UserRole.REGULAR_MODERATOR,
                UserRole.SENIOR_MODERATOR
            ),
                has_length(greater_than_or_equal_to(2))
            ),
            "rating": has_properties({
                "enabled": True,
                "quality": greater_than_or_equal_to(0),
                "quantity": greater_than_or_equal_to(0)
            })
        }
    ))

    # Reactivate user, as changing the email usually requires reactivation
    api.account.activate_registered_user(login=login)
