from faker import Faker
from hamcrest import assert_that, has_properties, greater_than_or_equal_to
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.roles import UserRole
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_put_v1_account_token():
    fake = Faker()
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host="http://5.63.153.31:5051")
    # Create user
    login = "Sasha" + str(fake.random_int(min=1, max=9999))
    registration_data = Registration(
        login=login,
        email=login + "@example.com",
        password="NewPass1234!"
    )
    api.account.post_v1_account(json=registration_data)

    # Get token from email and activate created user
    token = mailhog.get_token_from_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": has_properties({
                "enabled": True,
                "quality": greater_than_or_equal_to(0),
                "quantity": greater_than_or_equal_to(0)
            })
        }
    ))
