from faker import Faker
from hamcrest import has_properties, assert_that, greater_than_or_equal_to, all_of, only_contains, has_length
from dm_api_account.models.change_email_model import ChangeEmail
from dm_api_account.models.registration_model import Registration
from dm_api_account.models.roles import UserRole
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_put_v1_account_email():
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

    # Change user's email
    json = ChangeEmail(
        login=registration_data.login,
        password=registration_data.password,
        email=fake.company_email()
    )
    response_change_email = api.account.put_v1_account_email(json=json)
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

    # It is needed to activate user again after email changing
    upd_token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=upd_token)
