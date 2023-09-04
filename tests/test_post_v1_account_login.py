from datetime import datetime
from faker import Faker
from hamcrest import assert_that, has_properties, has_string, starts_with
from dm_api_account.models.login_credentials_model import LoginCredentials
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.roles import UserRole
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_post_v1_account_login():
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

    # Initial activation of user with token
    token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=token)

    # Login as user
    credentials = LoginCredentials(
        login=registration_data.login,
        password=registration_data.password,
        rememberMe=True
    )
    response_login = api.login.post_v1_account_login(json=credentials)
    assert_that(response_login.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.GUEST, UserRole.PLAYER],
            "rating": has_properties({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            }),
            "registration": has_string(starts_with(str(datetime.utcnow().date())))
        }
    ))
